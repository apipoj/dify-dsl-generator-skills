# เวอร์ชัน DSL สำหรับผลลัพธ์ใหม่

ตรวจสอบแหล่งข้อมูลวันที่ 17 กันยายน 2026 ผ่าน Exa และตรวจซ้ำกับ source ของ Dify โดยตรง เนื่องจากหน้า constants ที่ Exa เก็บไว้ยังแสดง `0.6.0`

| ชนิดผลลัพธ์ | เวอร์ชันที่ใช้ |
| --- | --- |
| `kind: app` โหมด `workflow` หรือ `advanced-chat` | `version: '0.7.0'` |
| `kind: rag_pipeline` | `version: '0.1.0'` |

ค่าต้องเป็น string ใช้เลขครบสามส่วน อย่าใช้ `version: 0.7` ซึ่ง YAML อาจอ่านเป็นตัวเลข และอย่าสับสนระหว่างเวอร์ชัน DSL กับเวอร์ชันโปรแกรม Dify หรือ `data.version` ของแต่ละโหนด

## ใช้กับการสร้างและการแก้ไข

- เมื่อสร้างใหม่ ให้ใช้เวอร์ชันตามตาราง ไม่คัดลอก header เก่าจาก fixture หรือ replay
- เมื่อตรวจไฟล์เก่า ให้รายงานเวอร์ชันจริง ห้ามแก้โดยไม่มีคำขอ
- เมื่อแก้ไฟล์เก่า อย่าเปลี่ยนเวอร์ชันเงียบ ๆ ระบุเวอร์ชันเป้าหมายและตรวจความเข้ากันได้ก่อนอัปเกรด หากผู้ใช้ต้องการคงเวอร์ชันเดิม ใช้ linter เดิมและรายงานว่าไม่ใช่ output contract ล่าสุด
- เก็บ `tests/fixtures/` และ replay เดิมไว้เป็น regression evidence ไม่ถือว่าเป็นตัวอย่างที่ผ่านการนำเข้าเวอร์ชันล่าสุด
- รัน `python3 scripts/validate_generated_dsl.py <output.yml>` จากราก repository หรือแพ็กเกจ โดยคำสั่งตรวจเวอร์ชัน ฟิลด์หลัก และ lint เท่านั้น
- รายงานแยกว่าผ่านการตรวจในเครื่อง ผ่านการนำเข้า Dify หรือผ่านการรันจริง ห้ามสรุปสองอย่างหลังจาก lint เพียงอย่างเดียว

## สิ่งที่เพิ่มใน 0.7.0

การเปลี่ยนแปลงที่เพิ่ม App DSL เป็น `0.7.0` เพิ่ม portable Agent Package schema v1 และการส่งออก Agent bindings ด้วย package references แทน ID ภายใน workspace จึงไม่ควรย้าย Agent รุ่นใหม่ด้วยการเปลี่ยน header อย่างเดียว

ชุดทักษะฉบับนี้ยังเน้น Workflow, Chatflow และ RAG Pipeline ตามขอบเขตเดิม ไม่ได้เพิ่มการสร้าง Agent App หรือรับรอง Agent v2/packages ทุกฟิลด์ หากพบ `agent_packages`, `agent_binding`, `agent_job` หรือ `agent-v2` ต้องตรวจ schema และการนำเข้าจริงเพิ่มเติม ห้ามแทนด้วย agent strategy แบบเดิมโดยอัตโนมัติ

## หลักฐานต้นทาง

- [ค่าคงที่ App DSL ณ commit ที่เปลี่ยนเป็น 0.7.0](https://github.com/langgenius/dify/blob/f86bfb2a31acb8c5398dc6beca04ac7326319b28/api/constants/dsl_version.py)
- [PR #38849 เพิ่ม Agent DSL import/export](https://github.com/langgenius/dify/pull/38849)
- [RAG Pipeline DSL service และเวอร์ชันแยก 0.1.0](https://github.com/langgenius/dify/blob/f86bfb2a31acb8c5398dc6beca04ac7326319b28/api/services/rag_pipeline/rag_pipeline_dsl_service.py)
- [App DSL import/export service](https://github.com/langgenius/dify/blob/f86bfb2a31acb8c5398dc6beca04ac7326319b28/api/services/app_dsl_service.py)
