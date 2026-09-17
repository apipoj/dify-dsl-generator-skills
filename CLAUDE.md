# Dify DSL ภาษาไทย

โปรเจกต์นี้เป็นชุด skill สำหรับออกแบบ สร้าง ตรวจ และแก้ Dify DSL ไม่ใช่ตัว Dify server

- ตอบและถามเป็นภาษาไทย เว้นแต่ผู้ใช้ขอภาษาอื่น
- สำหรับงาน Dify ให้เริ่มที่ `skills/using-dify-dsl/SKILL.md` และอ่านเฉพาะเอกสารที่เกี่ยวข้อง
- สร้าง App DSL ใหม่ด้วย `version: '0.7.0'` และ RAG Pipeline ด้วย `version: '0.1.0'` ตาม `skills/dify-dsl-foundations/references/dsl-version-policy.th.md`
- คง YAML keys, enum, node ID, selector, provider/model ID เป็นรูปแบบทางเทคนิคเดิม
- อย่าแปล technical references หรือ fixtures โดยอัตโนมัติ fixtures เป็นหลักฐาน regression ของต้นฉบับ ไม่ใช่แม่แบบเวอร์ชันล่าสุด
- คำสั่งที่ขึ้นต้น `scripts/`, `skills/` หรือ `tests/` อ้างอิงราก repository ถ้าใช้ skill ผ่าน symlink ให้ resolve พาธต้นทางก่อน อย่าสมมติว่ารากโปรเจกต์ผู้ใช้ตรงกับรากชุด skill
- ใช้ `python3 scripts/validate_generated_dsl.py <output.yml>` ตรวจผลลัพธ์ใหม่ และบอกว่าผลตรวจในเครื่องไม่ใช่การยืนยันว่านำเข้า Dify ได้แล้ว
- เมื่อต้องตรวจด้วย subagent ให้ใช้เฉพาะเครื่องมือที่มีและขอบเขตที่อนุญาต หากไม่มี ให้ระบุว่ายังไม่ได้ตรวจอิสระ
- เมื่อต้องแก้ชุด skill ให้ตรวจด้วย `python3 scripts/quick_validate.py`, `python3 scripts/validate_forward_testing.py` และ `python3 -m unittest discover -s tests -p 'test_*.py'`
