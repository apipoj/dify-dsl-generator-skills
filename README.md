# Dify DSL Skill Pack ฉบับภาษาไทย

ชุดทักษะสำหรับให้ AI ช่วยออกแบบ สร้าง ตรวจสอบ และแก้ไข Dify Workflow, Chatflow และ RAG Pipeline ใช้ได้กับ Claude Code, Claude.ai และ Codex

พัฒนาต่อยอดจาก [lazeyliu/dify-dsl-generator-skills](https://github.com/lazeyliu/dify-dsl-generator-skills) ภายใต้ [MIT License](LICENSE) ฉบับนี้แปล README คู่มือติดตั้ง และคำสั่งหลักทั้ง 12 skill เป็นไทย ส่วน technical references และ fixtures คงภาษาต้นฉบับ ปรับเฉพาะข้อกำหนดเวอร์ชันที่จำเป็นสำหรับการสร้างไฟล์ใหม่

[English](README.en.md) · [简体中文](README.zh-CN.md)

## เริ่มใช้กับ Claude Code

เปิด terminal ที่ราก repository ที่ clone มาแล้ว:

```bash
python3 scripts/install_claude_code.py
claude
```

สคริปต์จะสร้าง symlink ของทั้ง 12 skill ใน `.claude/skills/` ของโปรเจกต์ รันซ้ำได้โดยไม่ทำลาย skill อื่น หาก clone นี้มี symlink ครบอยู่แล้ว ก็เริ่ม `claude` ได้เลย

ลองพิมพ์ใน Claude Code:

```text
/using-dify-dsl สร้าง workflow รับข้อความภาษาไทยแล้วสรุปเป็น 3 ข้อ
ใช้โมเดลที่ฉันกำหนดและบันทึกเป็นไฟล์ YAML สำหรับนำเข้า Dify
```

หากยังไม่ได้ระบุโมเดลหรือข้อมูลที่จำเป็น ผู้ช่วยจะถามเฉพาะสิ่งที่ต้องใช้ การเรียก skill โดยตรงใช้ `/ชื่อ-skill` ดูขั้นตอนติดตั้งทุกโปรเจกต์และการแก้ปัญหาที่ [คู่มือ Claude](.claude/INSTALL.th.md)

## เริ่มใช้กับ Claude.ai

สร้างไฟล์สำหรับอัปโหลด:

```bash
python3 scripts/build_claude_ai_bundle.py
```

จะได้ `dist/dify-dsl-th.zip` ซึ่งรวมทางเข้าภาษาไทยทั้งชุด เอกสารอ้างอิง สคริปต์ และ fixtures โดยรักษาพาธภายใน

1. เปิดการสร้างไฟล์และรันโค้ดใน Settings > Capabilities ตามสิทธิ์ของบัญชี
2. ไปที่ Customize > Skills เลือกเพิ่ม skill แล้วเลือก Upload a skill
3. อัปโหลด `dist/dify-dsl-th.zip` และเปิดใช้งาน
4. เริ่มแชตแล้วขอว่า “ใช้ dify-dsl-th ช่วยสร้าง Dify workflow สำหรับ…”

ไม่ต้องอัปโหลดแต่ละ skill แยก เพราะมีการอ้างอิงข้ามโฟลเดอร์อยู่ในชุดเดียว หากใช้ Team หรือ Enterprise การเปิดใช้ขึ้นกับการตั้งค่าองค์กร ดู [วิธีใช้ Skills ของ Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

ใน Claude.ai ผู้ช่วยต้องตรวจเครื่องมือที่มีจริงก่อนเรียกสคริปต์หรือ subagent ถ้ารันไม่ได้ จะระบุส่วนที่ยังไม่ผ่านการตรวจ ห้ามถือว่าการอัปโหลด skill แปลว่าเชื่อมต่อ Dify แล้ว

## ใช้กับ Codex

```bash
bash scripts/install_codex_bundle.sh
```

เรียก `$using-dify-dsl` ตามด้วยโจทย์ ดู [คู่มือติดตั้ง Codex ภาษาไทย](.codex/INSTALL.th.md)

## เวอร์ชันไฟล์ที่สร้าง

- App DSL สำหรับ Workflow และ Chatflow ใช้ `version: '0.7.0'`
- RAG Pipeline ใช้เวอร์ชันแยก `version: '0.1.0'`
- เวอร์ชัน DSL ไม่ใช่เวอร์ชันตัวโปรแกรม Dify และไม่ใช่ `data.version` ของโหนด
- fixtures เดิมยังเก็บเวอร์ชันเก่าเพื่อใช้ทดสอบ regression ไม่ใช้ header เหล่านั้นกับงานใหม่

อ่าน [นโยบายเวอร์ชันและหลักฐานจาก Dify](skills/dify-dsl-foundations/references/dsl-version-policy.th.md) และดู [ตัวอย่าง Workflow ภาษาไทย](examples/echo-workflow-0.7.0.yml) ตัวอย่างรับข้อความแล้วส่งกลับโดยไม่ต้องตั้งค่าโมเดล

รองรับขอบเขตเดิมคือ Workflow, Chatflow และ RAG Pipeline การสร้าง Agent App และ portable Agent v2 packages ยังต้องตรวจ schema เพิ่มเติม ไม่ได้อ้างว่ารองรับทุกความสามารถของ DSL 0.7.0

## เลือก skill ตามงาน

| Skill | ใช้ทำอะไร |
| --- | --- |
| `using-dify-dsl` | เริ่มต้นและเลือกเส้นทางตามโจทย์ |
| `dify-dsl-brainstorming` | คลี่คลายความต้องการก่อนออกแบบ |
| `dify-dsl-authoring` | สร้างร่าง DSL จากโจทย์ชัดเจน |
| `dify-dsl-review` | ตรวจไฟล์เดิมแบบอ่านอย่างเดียว |
| `dify-dsl-refactor` | แก้ไขและปรับโครงสร้างไฟล์เดิม |
| `dify-dsl-subagent-review` | จัดการการตรวจอิสระเมื่อมีเครื่องมือและสิทธิ์ |
| `dify-dsl-foundations` | เลือกโหมดและกำหนดโครงสร้างพื้นฐาน |
| `dify-dsl-nodes` | เลือกโหนดและตรวจฟิลด์ |
| `dify-dsl-templates` | เลือกเทมเพลตและโครงร่าง |
| `dify-dsl-quality` | ค้นปัญหา จัดระดับ และเลือกวิธีแก้ |
| `dify-dsl-governance` | ประเมินความพร้อมส่งมอบ |
| `dify-dsl-forward-testing` | ประเมินการทำงานของชุด skill |

คำอธิบายและคำถามใช้ภาษาไทย ชื่อฟิลด์ YAML, enum, selector, node ID และ provider/model ID คงรูปแบบทางเทคนิคเดิม ข้อความบนหน้าจอและ prompt ใน workflow ใช้ไทยได้ตามโจทย์

## ตรวจสอบผลลัพธ์และชุด skill

ต้องมี Python 3.10 ขึ้นไปและ Ruby พร้อม YAML library สคริปต์เดิมใช้ Ruby ในการอ่าน YAML ไม่ต้องมี API key เพื่อรันการตรวจในเครื่อง

```bash
python3 scripts/validate_generated_dsl.py examples/echo-workflow-0.7.0.yml
python3 scripts/quick_validate.py
python3 scripts/validate_forward_testing.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

คำสั่งแรกตรวจเวอร์ชันผลลัพธ์ใหม่และ lint ส่วนการตรวจไฟล์เก่าให้ใช้ `python3 skills/dify-dsl-quality/scripts/lint_dsl.py <file.yml>` โดยไม่บังคับเปลี่ยนเวอร์ชัน

ผล lint และ replay ที่บันทึกไว้ไม่ใช่หลักฐานว่าได้รัน Claude ใหม่หรือนำเข้า Dify สำเร็จ ต้องตรวจการนำเข้าและรันกับ Dify ปลายทางอีกครั้งเมื่อมีการใช้งานจริง

## การพัฒนาต่อ

แก้ต้นฉบับที่ `skills/` แล้วสร้าง ZIP ใหม่ทุกครั้งที่เปลี่ยนเนื้อหา Claude Code ในโปรเจกต์ใช้ symlink จึงอ่านต้นฉบับเดียวกัน ส่วน Claude.ai ต้องอัปโหลด ZIP ที่สร้างใหม่เพื่ออัปเดต

repository นี้เป็นชุดทักษะ ไม่ใช่ Dify server และไม่ได้จัดเก็บ credentials ของ Dify การเผยแพร่เป็น fork หรือ repository ใหม่ทำแยกจากการตั้งค่าในเครื่อง
