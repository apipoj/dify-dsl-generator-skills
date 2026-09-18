# Codex และ Claude Code plugins

Plugin `dify-dsl-th` เวอร์ชัน `0.2.0` รวม 12 skills ภาษาไทย เอกสารอ้างอิง สคริปต์ตรวจ fixtures และตัวอย่าง Marketplace ชื่อ `apipoj-dify` ติดตั้งจาก repository ได้โดยตรง เวอร์ชัน plugin แยกจาก App DSL `0.7.0` และ RAG Pipeline `0.1.0`

## Claude Code

พิมพ์ใน Claude Code:

```text
/plugin marketplace add apipoj/dify-dsl-generator-skills
/plugin install dify-dsl-th@apipoj-dify
```

หรือรันใน terminal:

```bash
claude plugin marketplace add apipoj/dify-dsl-generator-skills
claude plugin install dify-dsl-th@apipoj-dify
```

เปิด session ใหม่แล้วเรียก `/dify-dsl-th:using-dify-dsl` ตามด้วยโจทย์ ดู [คู่มือ marketplace ของ Claude Code](https://code.claude.com/docs/en/plugin-marketplaces)

## Codex

```bash
codex plugin marketplace add apipoj/dify-dsl-generator-skills
codex plugin add dify-dsl-th@apipoj-dify
```

ต้องใช้ Codex รุ่นที่มีคำสั่ง `codex plugin` เปิด task ใหม่ แล้วขอ “ใช้ plugin dify-dsl-th โดยเริ่มจาก using-dify-dsl ช่วยสร้าง workflow สรุปข้อความภาษาไทย” ตรวจรายการด้วย `codex plugin list`

## อัปเดตและย้ายจากวิธีเดิม

Claude Code:

```bash
claude plugin marketplace update apipoj-dify
claude plugin update dify-dsl-th@apipoj-dify
```

Codex:

```bash
codex plugin marketplace upgrade apipoj-dify
codex plugin add dify-dsl-th@apipoj-dify
```

เปิด task/session ใหม่หลังอัปเดต หากติดตั้ง plugin เดิมจาก local marketplace `personal` ให้ถอนเฉพาะ plugin เดิมด้วย `codex plugin remove dify-dsl-th@personal` หรือ `claude plugin uninstall dify-dsl-th@personal` ตามแพลตฟอร์ม ก่อนติดตั้งจาก `apipoj-dify` ไม่ต้องลบ marketplace `personal` เพราะอาจมี plugin อื่น

หากเคยใช้ symlink ใน `.agents/skills/dify-dsl`, `~/.claude/skills` หรือ `.claude/skills` ให้เลือกช่องทางเดียวเพื่อไม่ให้ skill ซ้ำ การติดตั้งใหม่นี้ไม่ลบ symlink ให้

## สำหรับผู้พัฒนา

ผู้ใช้ทั่วไปไม่ต้อง build แพ็กเกจเอง Repository เก็บแพ็กเกจพร้อมติดตั้งใน `plugins/dify-dsl-th/` โดยสร้างจากต้นฉบับ `skills/`, `scripts/`, `tests/`, `docs/`, `examples/` และ manifest ใน `packaging/dify-dsl-th/` ไฟล์ประกอบอยู่ภายใน plugin ครบ ไม่อาศัย symlink ไปนอกแพ็กเกจ

หลังแก้ต้นฉบับ ให้ปรับเวอร์ชัน manifest ทั้งสองให้ตรงกันเมื่อออกรุ่นใหม่ แล้วรัน:

```bash
python3 scripts/sync_marketplace.py
python3 scripts/sync_marketplace.py --check
python3 -m unittest discover -s tests -p 'test_*.py'
claude plugin validate plugins/dify-dsl-th
claude plugin validate .claude-plugin/marketplace.json
```

Commit แพ็กเกจที่สร้างพร้อมต้นฉบับ CI ตรวจว่าแพ็กเกจตรงกับ source ห้ามแก้เฉพาะไฟล์ที่สร้างใน `plugins/dify-dsl-th/` เพราะจะถูกแทนที่ในการ sync ครั้งถัดไป

ยังสร้าง ZIP สำหรับแจกหรือติดตั้งจาก local marketplace ได้:

```bash
python3 scripts/build_plugin_bundle.py
python3 -m zipfile -e dist/dify-dsl-plugins.zip dist
```

จะได้ `dist/dify-dsl-plugins` ซึ่งมี catalog ชื่อ `apipoj-dify` เช่นเดียวกับ GitHub เลือกใช้แหล่งเดียวต่อ marketplace ชื่อนี้ หลีกเลี่ยงการลงทะเบียน local ทับ GitHub โดยไม่ตั้งใจ

## Claude.ai และขอบเขตความสามารถ

Claude.ai ใช้ `python3 scripts/build_claude_ai_bundle.py` แล้วอัปโหลด `dist/dify-dsl-th.zip` เป็น Skill ตาม [คู่มือติดตั้ง Claude](../.claude/INSTALL.th.md)

การรันสคริปต์ตรวจ DSL ต้องมี Python 3.10+ และ Ruby การติดตั้ง plugin ไม่ได้ติดตั้ง Dify server หรือเชื่อม API โดยอัตโนมัติ Role instructions สำหรับ review ไม่ได้ลงทะเบียนเป็น native custom agents ความสามารถเรียก subagent ขึ้นอยู่กับ host และเครื่องมือที่มีจริง การตรวจแพ็กเกจไม่ใช่หลักฐานว่า DSL นำเข้าและรันใน Dify ได้แล้ว
