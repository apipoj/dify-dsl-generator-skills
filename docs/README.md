# คู่มือ Dify DSL ภาษาไทย

เริ่มจาก [README หลัก](../README.md) สำหรับการติดตั้งและตัวอย่างคำสั่ง แล้วเลือกคู่มือตามงาน ชุดทักษะนี้ช่วยสร้างและตรวจ DSL แต่ไม่ได้เชื่อมต่อหรือนำเข้าไฟล์ไปยัง Dify โดยอัตโนมัติ

## คู่มือที่เกี่ยวข้อง

- [ติดตั้ง Claude Code และ Claude.ai](../.claude/INSTALL.th.md)
- [ติดตั้ง Codex](../.codex/INSTALL.th.md)
- [ภาพรวมการตรวจด้วยผู้ตรวจอิสระ](dify-dsl-subagent-review-overview.th.md) · [English](dify-dsl-subagent-review-overview.md) · [简体中文](dify-dsl-subagent-review-overview.zh-CN.md)
- [นโยบายเวอร์ชัน DSL และหลักฐานต้นทาง](../skills/dify-dsl-foundations/references/dsl-version-policy.th.md)
- [ตัวอย่าง Workflow ภาษาไทยแบบไม่ใช้โมเดล](../examples/echo-workflow-0.7.0.yml)

## เลือกเส้นทางตามโจทย์

<!-- BEGIN ROUTE_MATRIX -->
| เป้าหมาย | Skill เริ่มต้น | ขั้นตอนถัดไป |
| --- | --- | --- |
| ความต้องการยังไม่ชัดเจน | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-brainstorming](../skills/dify-dsl-brainstorming/SKILL.md) | `dify-dsl-authoring / review / refactor` |
| สร้าง DSL ใหม่ | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-authoring](../skills/dify-dsl-authoring/SKILL.md) | ใช้ `dify-dsl-subagent-review` เมื่อซับซ้อนหรือเสี่ยงสูง โดยตรวจเครื่องมือและสิทธิ์ก่อน |
| ตรวจ DSL เดิมแบบอ่านอย่างเดียว | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-review](../skills/dify-dsl-review/SKILL.md) | ใช้ `dify-dsl-subagent-review` เมื่อต้องตรวจอิสระหลายฝ่าย |
| แก้ไข DSL เดิม | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-refactor](../skills/dify-dsl-refactor/SKILL.md) | ใช้ `dify-dsl-subagent-review` เมื่อต้องตรวจอิสระหลังแก้ไข |
| เลือกเฉพาะเทมเพลต | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-templates](../skills/dify-dsl-templates/SKILL.md) | ไป `dify-dsl-authoring` เมื่อต้องสร้างร่าง DSL |
| ประเมินความพร้อมส่งมอบ | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-governance](../skills/dify-dsl-governance/SKILL.md) | ใช้ `dify-dsl-subagent-review` ก่อน เมื่อผู้ใช้ขอการตรวจหลายฝ่ายหรือรวมผลที่ขัดแย้ง |
| จัดการการตรวจหลายฝ่าย | [using-dify-dsl](../skills/using-dify-dsl/SKILL.md) หรือ [dify-dsl-subagent-review](../skills/dify-dsl-subagent-review/SKILL.md) | เลือกรูปแบบขนาน / ตามลำดับ / subagent เดียว / ไม่มี subagent ตามงาน เครื่องมือ และสิทธิ์ |
<!-- END ROUTE_MATRIX -->

ตารางนี้สร้างจาก [ข้อมูลเส้นทางร่วม](dify-dsl-route-matrix.json) เพื่อให้คู่มือไทย อังกฤษ และจีนใช้เส้นทางเดียวกัน

## ขอบเขตแต่ละแพลตฟอร์ม

| แพลตฟอร์ม | การติดตั้งในโปรเจกต์นี้ | การตรวจอิสระ |
| --- | --- | --- |
| Claude Code | ลิงก์ 12 skill ผ่าน `.claude/skills/` | ใช้ subagent ที่เครื่องมือและสิทธิ์ของเซสชันรองรับ โดยส่งบทบาทและไฟล์ที่ต้องอ่านให้ครบ |
| Claude.ai | อัปโหลด `dist/dify-dsl-th.zip` เป็น skill เดียว | ตรวจว่ามีเครื่องมือสร้างผู้ตรวจอิสระจริง หากไม่มี ให้ตรวจด้วยผู้ช่วยตัวเดียวและแจ้งข้อจำกัด |
| Codex | ติดตั้งชุด skill ผ่าน `~/.agents/skills/dify-dsl` | ใช้เครื่องมือ subagent ตามสิทธิ์ของเซสชัน หากใช้ไม่ได้ ให้ใช้โหมดไม่มี subagent |

ไฟล์ใน `skills/dify-dsl-quality/agents/` เป็นคำอธิบายบทบาท ยังไม่ใช่ custom agent ที่ติดตั้งใน `.claude/agents/` สคริปต์ติดตั้งของเราสร้างเฉพาะลิงก์ skill หากจะใช้ชื่อ custom agent โดยตรง ต้องตั้งค่า agent แยกก่อน หรือส่งคำอธิบายบทบาทให้ subagent ที่มีอยู่ [เอกสาร Claude Code](https://code.claude.com/docs/en/sub-agents)

การอัปโหลด skill ใน Claude.ai ให้ความรู้และขั้นตอนแก่ผู้ช่วย ไม่ใช่หลักฐานว่ามีเครื่องมือทุกชนิดในเซสชัน การใช้ Skills ต้องเปิดความสามารถรันโค้ดตามการตั้งค่าบัญชีหรือองค์กร [เอกสาร Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## เวอร์ชันผลลัพธ์

App DSL ในโหมด `workflow` และ `advanced-chat` ใช้ `version: '0.7.0'` ส่วน `rag_pipeline` ใช้ `version: '0.1.0'` แยกกัน อย่าใช้เลขเวอร์ชันของตัวโปรแกรม Dify หรือ `data.version` ของโหนดแทน

ชุดทักษะยังไม่ได้รับรองการสร้าง Agent App หรือ portable Agent v2 packages ทุกฟิลด์ ตรวจขอบเขตและหลักฐานใน [นโยบายเวอร์ชัน](../skills/dify-dsl-foundations/references/dsl-version-policy.th.md) ก่อนใช้ ส่วน fixtures และ replay เดิมเก็บไว้เป็นหลักฐาน regression ไม่ใช่แม่แบบเวอร์ชันล่าสุด

## ผลตรวจแต่ละแบบบอกอะไร

| วิธีตรวจ | ยืนยันได้ | ยังยืนยันไม่ได้ |
| --- | --- | --- |
| `quick_validate.py` | โครงสร้าง skill ลิงก์ใน skill และตารางที่สร้างอัตโนมัติสอดคล้องกัน | พฤติกรรมของโมเดลจริง |
| `validate_forward_testing.py` | case, lint และข้อกำหนดของ replay ที่บันทึกไว้ผ่าน | การรัน Claude ใหม่หรือผู้ตรวจอิสระจริงในรอบนี้ |
| `validate_generated_dsl.py` | เวอร์ชันผลลัพธ์และกฎ lint ที่สคริปต์ครอบคลุม | การนำเข้าและการรันบน Dify ปลายทาง |
| ทดสอบบนแพลตฟอร์มจริง | พฤติกรรมที่สังเกตได้ในเซสชันหรือ Dify ที่ทดสอบ | ผลกับทุกเวอร์ชัน โมเดล หรือสภาพแวดล้อม |

รันคำสั่งจากราก repository โดยต้องมี Python 3.10+ และ Ruby สำหรับสคริปต์ตรวจ YAML รายงานสิ่งที่ตรวจจริงแยกจากสิ่งที่ยังไม่ได้ตรวจเสมอ

## แก้ไขคู่มือ

แก้ข้อความเส้นทางใน `dify-dsl-route-matrix.json` ที่ฟิลด์ `goal_th`, `next_th`, `main_path_th` และภาษาที่เกี่ยวข้อง แล้วรัน:

```bash
python3 scripts/route_matrix_docs.py --write
python3 scripts/quick_validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build_claude_ai_bundle.py
```

อย่าแก้ตารางระหว่าง marker โดยตรง เพราะการสร้างใหม่จะเขียนทับ แก้เนื้อหาคู่มือส่วนอื่นได้ตามปกติ และสร้าง ZIP ใหม่หลังแก้เพื่อให้ผู้ใช้ Claude.ai ได้เอกสารชุดล่าสุด

ตรวจสอบแหล่งข้อมูลแพลตฟอร์มผ่าน Exa วันที่ 17 กันยายน 2026
