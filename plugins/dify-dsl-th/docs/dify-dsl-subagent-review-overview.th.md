# ภาพรวมการตรวจ Dify DSL ด้วยผู้ตรวจอิสระ

[คู่มือทั้งหมด](README.md) · [English](dify-dsl-subagent-review-overview.md) · [简体中文](dify-dsl-subagent-review-overview.zh-CN.md)

`dify-dsl-subagent-review` จัดการการตรวจแบบอ่านอย่างเดียว เลือกรูปแบบการตรวจตามงาน เครื่องมือ และสิทธิ์ แล้วรวมความเห็นที่ขัดแย้งกัน หน้าที่หลักยังอยู่ที่ `authoring`, `review`, `refactor` หรือ `governance` ตามโจทย์

## เริ่มใช้เมื่อใด

ใช้เมื่อมีร่างหรือ DSL เดิมแล้ว และต้องการตรวจอิสระหลายฝ่าย แยกการตรวจฟิลด์ กราฟ prompt หรือความพร้อมส่งมอบ รวมถึงเมื่อต้องรวมข้อสรุปที่ขัดกัน

หากโจทย์ยังไม่ชัด ให้กลับไป brainstorming หากยังไม่มีร่าง ให้สร้างด้วย authoring ก่อน งานตรวจทั่วไปที่ผู้ช่วยตัวเดียวตรวจได้เพียงพอไม่จำเป็นต้องเพิ่มผู้ตรวจหลายฝ่าย

## เส้นทางหลัก

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

<!-- BEGIN MAIN_PATH -->
```text
using-dify-dsl
-> brainstorming / authoring / review / refactor / templates / governance / subagent-review
-> ตรวจต่อด้วย subagent-review หรือ governance เฉพาะเมื่อจำเป็น
```
<!-- END MAIN_PATH -->

## ความสัมพันธ์กับ skill อื่น

| Skill | หน้าที่ |
| --- | --- |
| `using-dify-dsl` | เลือกประเภทงานและเส้นทางเริ่มต้น |
| `dify-dsl-authoring` | สร้างร่างก่อนส่งตรวจ |
| `dify-dsl-review` | ตรวจแบบอ่านอย่างเดียว และส่งต่อเมื่อจำเป็นต้องตรวจหลายฝ่าย |
| `dify-dsl-refactor` | แก้ไขตามขอบเขตที่อนุญาต แล้วส่งผลให้ตรวจอิสระ |
| `dify-dsl-governance` | ประเมินการส่งมอบจากผลตรวจและหลักฐาน |

## รูปแบบการตรวจ 4 แบบ

| รูปแบบ | ใช้เมื่อ | วิธีทำ |
| --- | --- | --- |
| ขนาน | หลายด้านตรวจแยกกันได้ และต้องการความเห็นอิสระ | แยกตรวจฟิลด์ กราฟ และ prompt กับข้อมูลเข้าออก |
| ตามลำดับ | ผลรอบถัดไปขึ้นกับข้อสรุปก่อนหน้า | ตรวจโครงสร้างและฟิลด์ก่อน ตามด้วย prompt แล้วรวมเกณฑ์ส่งมอบเมื่อจำเป็น |
| subagent เดียว | ปัญหาอยู่ในขอบเขตแคบ เช่น selector อ้างโหนดที่ไม่มี | ส่งเฉพาะบทบาทที่เกี่ยวข้อง ห้ามอ้างว่าเป็นการตรวจหลายฝ่าย |
| ไม่มี subagent | ไม่มีเครื่องมือ เซสชันไม่อนุญาต หรือผู้ใช้ห้าม | ตรวจด้วยผู้ช่วยตัวเดียว ระบุว่า “ยังไม่ได้ตรวจโดยผู้ตรวจอิสระ” และให้ข้อสรุปอย่างน้อยว่าต้องยืนยันโดยมนุษย์ |

อ่าน [ตารางเลือกรูปแบบฉบับเทคนิค](../skills/dify-dsl-subagent-review/references/mode-selection-matrix.md) เมื่อจำเป็น อย่าเลือกขนานเพียงเพราะมีหลายบทบาท หากงานต้องรอผลกันให้ใช้ตามลำดับ

## บทบาทของผู้ตรวจ

- **ฟิลด์และข้อกำหนด** ตรวจชนิด ค่า และฟิลด์ที่จำเป็น
- **กราฟและเส้นทางการทำงาน** ตรวจ edge, selector, container และเส้นทางที่เข้าถึงได้
- **Prompt และข้อมูลเข้าออก** ตรวจข้อตกลงข้อมูลและพฤติกรรมที่คาดหวัง
- **ความพร้อมเผยแพร่** ใช้เพิ่มเมื่อสามฝ่ายแรกเห็นไม่ตรงกัน หรือต้องรวมเกณฑ์ส่งมอบ ความครอบคลุม และการติดตามระบบ

ใช้ [คำอธิบายบทบาทต้นฉบับ](../skills/dify-dsl-quality/agents/index.md) และส่งไฟล์ที่เกี่ยวข้องให้ผู้ตรวจแต่ละตัว ห้ามให้ผู้ตรวจแก้ DSL ระหว่างตรวจ และห้ามเรียกผู้ช่วยตัวเดียวตรวจหลายรอบแล้วนับเป็นผู้ตรวจอิสระหลายฝ่าย

## Claude Code, Claude.ai และ Codex

การติดตั้ง skill ไม่ได้ติดตั้ง custom agent ชื่อเดียวกับบทบาทโดยอัตโนมัติ ใน repository นี้ไม่มี `.claude/agents/` สำหรับสี่บทบาทดังกล่าว สามารถส่งคำอธิบายบทบาทให้ subagent ที่มีอยู่ หรือสร้าง custom agent แยกเมื่อจำเป็น โดยจำกัดเครื่องมือให้อยู่ในขอบเขตอ่านอย่างเดียว [เอกสาร Claude Code](https://code.claude.com/docs/en/sub-agents)

ใน Claude.ai และ Codex ให้ตรวจเครื่องมือและสิทธิ์ของเซสชันจริง หากสร้างผู้ตรวจอิสระไม่ได้ ให้ลดรูปแบบ `3 -> 1 -> 0` ตามสิ่งที่ทำได้และแจ้งเหตุผล อย่ารับรองความสามารถจากชื่อแพลตฟอร์มหรือจากการอัปโหลด ZIP เพียงอย่างเดียว ดู [ขอบเขตแพลตฟอร์มและการติดตั้ง](README.md)

## หลักฐานที่มีใน repository

| สิ่งที่ครอบคลุม | Case ที่บันทึกไว้ |
| --- | --- |
| การจัดการตรวจและรวมเกณฑ์ส่งมอบ | `orchestrate-readonly-review`, `merge-release-readiness` |
| ไม่มี subagent | `degrade-no-subagent` |
| ความเห็น review กับ governance ขัดกัน | `merge-rag-review-vs-governance`, `merge-chat-review-vs-governance` |
| เลือกตามลำดับหรือผู้ตรวจเดียว | `select-serial-chat-review`, `select-single-graph-review` |
| การส่งต่อจาก skill อื่น | `route-to-subagent-review`, `route-full-lifecycle-rag`, `knowledge-retrieval-authoring-needs-review`, `refactor-retrieval-topk-needs-review` |

รายการนี้เป็น case และ replay ที่เก็บไว้ การรัน `validate_forward_testing.py` ตรวจโครงสร้าง case, lint และ replay assertions ไม่ได้เรียก Claude หรือเปิดผู้ตรวจใหม่ จึงต้องทดสอบบนแพลตฟอร์มจริงแยกต่างหากก่อนอ้างว่าทำงานครบวงจร

การผ่าน lint ยังไม่ยืนยันการนำเข้าหรือรันบน Dify และ fixtures เก่าอาจใช้ header ต่างจากผลลัพธ์ใหม่ อ่าน [นโยบาย DSL 0.7.0 และขอบเขต Agent v2](../skills/dify-dsl-foundations/references/dsl-version-policy.th.md) ก่อนสรุปความเข้ากันได้

## สิ่งที่ควรรายงาน

ระบุงานหลัก รูปแบบที่เลือกและเหตุผล จำนวนกับชื่อผู้ตรวจที่ใช้งานจริง ปัญหาของแต่ละบทบาท จุดขัดแย้งและผลตัดสิน ข้อสรุปรวม และความเสี่ยงคงเหลือ หากลดรูปแบบการตรวจหรือรันสคริปต์ไม่ได้ ต้องบอกตามจริง

## อ่านต่อ

1. [ทางเข้าหลัก](../skills/using-dify-dsl/SKILL.md)
2. [Skill สำหรับจัดการการตรวจ](../skills/dify-dsl-subagent-review/SKILL.md)
3. [ขั้นตอนการจัดการตรวจฉบับเทคนิค](../skills/dify-dsl-subagent-review/references/orchestration-playbook.md)
4. [แนวทางตรวจอิสระฉบับเทคนิค](../skills/dify-dsl-quality/references/subagent-review.md)

เอกสารเชิงเทคนิคที่ลิงก์ไว้คงภาษาต้นฉบับ ตรวจสอบแหล่งข้อมูลแพลตฟอร์มผ่าน Exa วันที่ 17 กันยายน 2026
