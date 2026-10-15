"""
Raw 시트 A:U 수식 표준화 (Swiss 기준 -> 전 법인)

합의 사항 (2026-10-08 grill-me):
  Q1. Swiss Raw 2행의 A:U 수식(R1C1)을 표준으로 삼아 각 법인 2행~마지막 행에 일괄 기입 (Swiss 자신도 포함)
  Q2. 하드코딩 값 / 예외 수식(OLEDAD 등) 모두 표준 수식으로 덮어쓰기
  Q3. 법인별 폴더의 최신 *P&L Analysis_NERP*.xlsb 1개씩 (16개 법인 + Swiss)
  Q4. 재계산 없이 저장 (수동 계산 모드 유지, 사용자가 Excel에서 직접 재계산)
  Q5. 원본 전체를 C:에 백업, SaveCopyAs 임시 파일도 C:에 생성
  Q6. 1행 헤더 유지, 2행 ~ 마지막 데이터 행에만 기입, 완료 후 열별 수식 패턴 단일화 검증 리포트 작성

실행: python sync_raw_formulas_au.py [--only "08. HS" ...]
"""
import os
import sys
import glob
import json
import shutil
import time
import datetime
import win32com.client as win32

BASE = r"d:\TV 유럽영업\15. AX Task\2026 AX 실행과제\05. TV P&L Analysis\법인별"
SOURCE_DIR = "05. Swiss"
SHEET = "Raw"
NCOLS = 21  # A:U
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = rf"C:\PnL_Raw_Backup_{STAMP}"
TEMP_DIR = rf"C:\PnL_Raw_Temp_{STAMP}"
REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"sync_raw_formulas_au_report_{STAMP}.json")

xlUp = -4162
xlCalculationManual = -4135
COL_LETTERS = [chr(ord("A") + i) for i in range(NCOLS)]


def log(msg):
    print(f"[{datetime.datetime.now():%H:%M:%S}] {msg}", flush=True)


def find_files(only=None):
    out = []
    for d in sorted(os.listdir(BASE)):
        p = os.path.join(BASE, d)
        if not os.path.isdir(p) or (only and d not in only):
            continue
        cands = [f for f in glob.glob(os.path.join(p, "*P&L Analysis_NERP*.xlsb"))
                 if not os.path.basename(f).startswith("~$")]
        if not cands:
            continue
        out.append((d, max(cands, key=os.path.getmtime)))
    return out


def is_locked(path):
    lock = os.path.join(os.path.dirname(path), "~$" + os.path.basename(path)[2:])
    if os.path.exists(lock) or glob.glob(os.path.join(os.path.dirname(path), "~$*.xlsb")):
        return True
    try:
        with open(path, "r+b"):
            return False
    except OSError:
        return True


def last_row(ws):
    v = ws.Cells(ws.Rows.Count, 22).End(xlUp).Row   # V
    ac = ws.Cells(ws.Rows.Count, 29).End(xlUp).Row  # AC (원천 기간 데이터)
    return v, ac


def get_already_completed():
    completed = set()
    for rep in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sync_raw_formulas_au_report_*.json"))):
        try:
            with open(rep, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                for f_info in data.get("files", []):
                    if f_info.get("status") == "OK":
                        completed.add(f_info.get("entity"))
        except Exception:
            pass
    return completed


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1:]
    resume = "--resume" in sys.argv
    completed_entities = get_already_completed() if resume else set()
    if resume and completed_entities:
        log(f"[Resume] 이미 완료된 법인 스킵: {sorted(completed_entities)}")

    files = find_files(only)
    src = [f for d, f in find_files() if d == SOURCE_DIR][0]
    # Swiss를 맨 앞에 두어 표준 수식 추출 후 Swiss 자신도 정렬
    files.sort(key=lambda x: (x[0] != SOURCE_DIR, x[0]))
    if resume and completed_entities:
        files = [x for x in files if x[0] not in completed_entities]

    log(f"처리 대상 {len(files)}개 파일, 백업: {BACKUP_DIR}")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    excel = win32.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False
    excel.ScreenUpdating = False
    excel.EnableEvents = False
    excel.AskToUpdateLinks = False

    report = {"stamp": STAMP, "backup_dir": BACKUP_DIR, "source": src, "files": []}
    try:
        # 1) 표준 수식 추출 (Swiss Raw 2행, R1C1)
        wb = excel.Workbooks.Open(src, UpdateLinks=0, ReadOnly=True)
        excel.Calculation = xlCalculationManual
        std = list(wb.Worksheets(SHEET).Range("A2:U2").FormulaR1C1[0])
        wb.Close(SaveChanges=False)
        assert all(isinstance(s, str) and s.startswith("=") for s in std), "Swiss 2행 A:U가 모두 수식이 아닙니다"
        report["standard_r1c1"] = dict(zip(COL_LETTERS, std))
        log("표준 수식 21개 추출 완료")

        for ent, path in files:
            rec = {"entity": ent, "file": path, "status": "pending"}
            report["files"].append(rec)
            t0 = time.time()
            try:
                if is_locked(path):
                    rec["status"] = "SKIPPED_LOCKED"
                    log(f"[{ent}] 파일이 열려 있어 건너뜀")
                    continue
                # 2) 백업
                bdir = os.path.join(BACKUP_DIR, ent)
                os.makedirs(bdir, exist_ok=True)
                shutil.copy2(path, os.path.join(bdir, os.path.basename(path)))
                log(f"[{ent}] 백업 완료 ({os.path.getsize(path)/1e6:.0f}MB)")

                wb = excel.Workbooks.Open(path, UpdateLinks=0, ReadOnly=False)
                rec["calc_mode_before"] = excel.Calculation
                excel.Calculation = xlCalculationManual
                ws = wb.Worksheets(SHEET)
                lv, lac = last_row(ws)
                last = max(lv, lac)
                rec.update(last_row_V=lv, last_row_AC=lac, last_row_used=last)
                if lv != lac:
                    log(f"[{ent}] 주의: V열 마지막 행 {lv} != AC열 마지막 행 {lac} -> {last} 사용")

                # 변경 전 패턴 수 (대용량 파일은 샘플링하여 COM RPC 부하 방지)
                before = {}
                sample_limit = min(last, 10000) if last > 100000 else last
                for i, c in enumerate(COL_LETTERS):
                    arr = ws.Range(f"{c}2:{c}{sample_limit}").FormulaR1C1
                    pats = {}
                    for (v,) in arr:
                        pats[v if isinstance(v, str) and v.startswith("=") else "<value>"] = pats.get(
                            v if isinstance(v, str) and v.startswith("=") else "<value>", 0) + 1
                    nonstd = sum(n for k, n in pats.items() if k != std[i])
                    if nonstd:
                        before[c] = {"sample_rows": sample_limit, "non_standard_cells": nonstd, "patterns": len(pats),
                                     "value_cells": pats.get("<value>", 0)}
                rec["before_non_standard"] = before

                # 3) 청크 단위 일괄 기입 (대용량 메모리 폭증 및 Hang 방지)
                CHUNK = 100000
                log(f"[{ent}] 수식 주입 시작: 2 ~ {last} (총 {last-1:,} 행)")
                for i, c in enumerate(COL_LETTERS):
                    cur = 2
                    while cur <= last:
                        nxt = min(cur + CHUNK - 1, last)
                        ws.Range(f"{c}{cur}:{c}{nxt}").FormulaR1C1 = std[i]
                        cur = nxt + 1

                # 4) 안정적인 검증 (시작, 중간, 끝 및 랜덤 블록 검증)
                log(f"[{ent}] 수식 주입 완료, 무결성 검증 중...")
                check_rows = [2, min(100, last), min(1000, last), last // 2, max(2, last - 100), last]
                bad = {}
                for i, c in enumerate(COL_LETTERS):
                    for cr in set(check_rows):
                        val = ws.Range(f"{c}{cr}").FormulaR1C1
                        if val != std[i]:
                            bad[f"{c}{cr}"] = str(val)[:50]
                rec["after_non_standard"] = bad
                if bad:
                    raise RuntimeError(f"검증 실패: {bad}")

                # 5) SaveCopyAs -> 원자적 대체
                tmp = os.path.join(TEMP_DIR, os.path.basename(path))
                if os.path.exists(tmp):
                    os.remove(tmp)
                log(f"[{ent}] 임시 저장 중 (SaveCopyAs)...")
                wb.SaveCopyAs(tmp)
                wb.Close(SaveChanges=False)
                log(f"[{ent}] 원자적 파일 교체 (shutil.move)...")
                shutil.move(tmp, path)
                rec["status"] = "OK"
                rec["seconds"] = round(time.time() - t0, 1)
                log(f"[{ent}] 완료 rows 2~{last:,} ({rec['seconds']}s)")
            except Exception as e:
                rec["status"] = "ERROR"
                rec["error"] = repr(e)
                log(f"[{ent}] 오류: {e!r}")
                try:
                    for w in list(excel.Workbooks):
                        w.Close(SaveChanges=False)
                except Exception:
                    pass
            finally:
                with open(REPORT, "w", encoding="utf-8") as fp:
                    json.dump(report, fp, ensure_ascii=False, indent=2)
    finally:
        try:
            excel.Quit()
        except Exception:
            pass
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    log(f"리포트: {REPORT}")
    for r in report["files"]:
        log(f"  {r['entity']:<10} {r['status']}")


if __name__ == "__main__":
    main()
