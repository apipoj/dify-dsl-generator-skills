# Codex และ Claude Code plugins

แพ็กเกจ `dify-dsl-th` เวอร์ชัน `0.1.0` รวม 12 skills ภาษาไทย เอกสารอ้างอิง สคริปต์ตรวจ fixtures และตัวอย่างไว้ใน plugin เดียว ใช้ได้ทั้ง Codex และ Claude Code โดยแต่ละแพลตฟอร์มอ่าน manifest ของตัวเอง เวอร์ชัน plugin แยกจาก App DSL `0.7.0` และ RAG Pipeline `0.1.0`

## สร้างแพ็กเกจ

ต้องมี Python 3.10+ สำหรับ build และ Ruby สำหรับสคริปต์ตรวจ DSL ใช้ terminal ที่ราก repository:

```bash
python3 scripts/build_plugin_bundle.py
python3 -m zipfile -e dist/dify-dsl-plugins.zip dist
```

จะได้ local marketplace ใน `dist/dify-dsl-plugins` และ plugin ที่ `dist/dify-dsl-plugins/plugins/dify-dsl-th` ไฟล์ทั้งหมดเป็นไฟล์จริง ไม่มี symlink กลับไปยัง source repository จึงย้ายทั้งโฟลเดอร์ marketplace ไปเก็บในตำแหน่งถาวรได้ก่อนติดตั้ง อย่าลบโฟลเดอร์ที่ใช้ลงทะเบียน marketplace

ZIP เดียวกันติดตั้งได้ทั้งสองแพลตฟอร์ม GitHub Actions แนบไฟล์นี้ใน artifact ชื่อ `dify-dsl-plugins` หลัง build ผ่าน หากดาวน์โหลด artifact ให้แตก ZIP ชั้นนอกก่อน แล้วแตก `dify-dsl-plugins.zip`

## Codex

จากราก repository หลังแตก ZIP:

```bash
codex plugin marketplace add ./dist/dify-dsl-plugins
codex plugin add dify-dsl-th@personal
```

เปิด task ใหม่ แล้วขอ “ใช้ using-dify-dsl ช่วยสร้าง workflow สรุปข้อความภาษาไทย” ตรวจรายการด้วย `codex plugin list` ต้องใช้ Codex รุ่นที่มีคำสั่ง `codex plugin`

## Claude Code

```bash
claude plugin marketplace add ./dist/dify-dsl-plugins
claude plugin install dify-dsl-th@personal
```

เปิด Claude Code session ใหม่ แล้วเรียก:

```text
/dify-dsl-th:using-dify-dsl สร้าง workflow สรุปข้อความภาษาไทยเป็น 3 ข้อ
```

ทดสอบแบบไม่ติดตั้งถาวรได้ด้วย `claude --plugin-dir ./dist/dify-dsl-plugins/plugins/dify-dsl-th` ดู [คู่มือ plugin ของ Claude Code](https://code.claude.com/docs/en/plugins-reference)

## การติดตั้งเดิมและการอัปเดต

- Marketplace ที่สร้างใช้ชื่อ `personal` หากมี marketplace ชื่อนี้อยู่แล้ว ให้ใช้ชื่อที่ไม่ซ้ำในฟิลด์ `name` ของ catalog ทั้งสองไฟล์ก่อนลงทะเบียน และใช้ชื่อนั้นแทน `@personal` อย่าแทนที่ marketplace เดิมโดยไม่ตรวจสอบ
- หากเคยติดตั้งด้วย symlink ใน `.agents/skills/dify-dsl`, `~/.claude/skills` หรือ `.claude/skills` ของโปรเจกต์ ให้เลือกใช้ช่องทางเดียวเพื่อไม่ให้เห็น skill ซ้ำ แพ็กเกจนี้ไม่ลบการติดตั้งเดิมให้
- Source ของ skills อยู่ที่ `skills/` และ manifest ต้นฉบับอยู่ที่ `packaging/dify-dsl-th/` อย่าแก้ไฟล์ใน `dist/` เพื่อพัฒนา
- เมื่อออก plugin เวอร์ชันใหม่ ให้เปลี่ยน `version` ของ manifest ทั้งสองให้ตรงกัน build ใหม่ แล้วแตกทับในตำแหน่ง marketplace เดิม สำหรับ Claude Code ใช้ `claude plugin marketplace update personal` และ `claude plugin update dify-dsl-th@personal` สำหรับ Codex ใช้ `codex plugin add dify-dsl-th@personal` แล้วเปิด task/session ใหม่
- Repository ต้นทางเป็น source สำหรับ build; คำสั่ง marketplace add ต้องชี้ไปที่โฟลเดอร์ที่แตกแพ็กเกจแล้ว ไม่ใช่ URL ของ repository

## Claude.ai และขอบเขตความสามารถ

Claude.ai ยังใช้ `python3 scripts/build_claude_ai_bundle.py` และอัปโหลด `dist/dify-dsl-th.zip` เป็น Skill ตาม [คู่มือติดตั้ง Claude](../.claude/INSTALL.th.md) ไม่ใช่ ZIP ของ native plugin

Plugin นี้เพิ่มทักษะสร้างและตรวจ Dify DSL ไม่ได้ติดตั้ง Dify server หรือเชื่อม API โดยอัตโนมัติ Role instructions สำหรับ review ไม่ได้ลงทะเบียนเป็น native custom agents ความสามารถเรียก subagent ขึ้นอยู่กับ host และเครื่องมือที่มีจริง การตรวจแพ็กเกจไม่ใช่หลักฐานว่า DSL นำเข้าและรันใน Dify ได้แล้ว

## ตรวจแพ็กเกจในเครื่อง

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
claude plugin validate ./dist/dify-dsl-plugins/plugins/dify-dsl-th
claude plugin validate ./dist/dify-dsl-plugins/.claude-plugin/marketplace.json
```

Tests ตรวจการแตกแพ็กเกจ ความครบของ skills และ relative links ความสอดคล้องของ manifests และรัน DSL validator จากแพ็กเกจใน working directory อื่น
