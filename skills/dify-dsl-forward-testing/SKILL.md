---
name: dify-dsl-forward-testing
description: ประเมินตัว skill ของ Dify DSL ด้วยตัวอย่างจริง คำขอจริง และการไม่เปิดเผยคำตอบที่คาดหวัง ใช้ตรวจการทำงานร่วมกันของ authoring, review, refactor และ templates ไม่ใช่การทดสอบ workflow บน Dify จริง
---

# dify-dsl-forward-testing

ให้ skill เป็นสิ่งที่ถูกทดสอบ อย่าทำให้ prompt กลายเป็นคำใบ้เฉลย

## เริ่มอ่าน

อ่าน [ดัชนีอ้างอิง](references/index.md) แล้วเลือกสคริปต์ตามงาน คำสั่งด้านล่างอ้างอิงจากราก repository หรือรากแพ็กเกจที่มีโฟลเดอร์ `skills/` และ `tests/` ไม่ใช่ working directory ของผู้ใช้โดยอัตโนมัติ

## สคริปต์

- `python3 skills/dify-dsl-foundations/scripts/fast_test_dsl.py <sample.yml>`
- `python3 skills/dify-dsl-foundations/scripts/fast_test_suite.py <sample.yml|directory> [...]`
- `python3 skills/dify-dsl-forward-testing/scripts/init_forward_test_case.py <case-dir> --target <sample.yml>`
- `python3 skills/dify-dsl-forward-testing/scripts/check_forward_test_cases.py <cases-root> [repo-root]`
- `python3 skills/dify-dsl-forward-testing/scripts/check_replay_outputs.py <case-dir> [...] [--repo-root <repo-root>]`
- `python3 skills/dify-dsl-forward-testing/scripts/run_validation_suite.py [<cases-root> ...] [--repo-root <repo-root>] [--json-out <report.json>]`
- `python3 skills/dify-dsl-forward-testing/scripts/compare_validation_reports.py <old.json> <new.json> [--json-out <diff.json>]`

## ข้อกำหนด

- อย่าเปิดเผยคำตอบใน `oracle.json` ให้เซสชันที่ถูกทดสอบ
- อย่าแก้ prompt ให้ชี้นำคำตอบเพียงเพื่อให้ผ่าน
- ทดสอบเป้าหมายหลักเดียวต่อรอบ เช่น การเลือกเส้นทาง การตรวจ การเลือกเทมเพลต หรือวิธีปรับโครงสร้าง
- ผูก `replay-output.txt` และ `expectation_files` กับ case เพื่อให้ตรวจผลได้ด้วยเครื่อง
- ใช้ `run_validation_suite.py` สำหรับ regression เพื่อเช็กโครงสร้าง case และ replay assertions
- ใช้ `--json-out` เมื่อต้องส่งผลให้ CI หรือแพลตฟอร์มอื่น
- เปรียบเทียบรายงานด้วย `compare_validation_reports.py` หรือส่ง `--baseline-report` และ `--diff-json-out` ให้ validation suite
- การตรวจ replay ที่บันทึกไว้ไม่เท่ากับการรัน agent ใหม่ หากไม่ได้ทดสอบบน Claude Code, Claude.ai หรือ Dify จริง ต้องระบุให้ชัด
