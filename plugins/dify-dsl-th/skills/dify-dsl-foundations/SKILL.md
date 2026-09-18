---
name: dify-dsl-foundations
description: พื้นฐานร่วมของ Dify DSL สำหรับเลือกโหมดและเส้นทางงาน กำหนด selector ฟิลด์ รูปแบบผลลัพธ์ และเกณฑ์ตรวจสอบ ใช้ก่อน authoring, review และ refactor
---

# dify-dsl-foundations

ระบุโหมด เส้นทางงาน และรูปแบบฟิลด์กับผลลัพธ์ให้ชัด ก่อนลงรายละเอียดโหนด เทมเพลต คุณภาพ หรือการส่งมอบ

## เริ่มอ่าน

อ่าน [ดัชนีอ้างอิง](references/index.md) แล้วเลือกเฉพาะ `common-dsl / task-routing / orchestration-modes / selector-templates / output-contract / validation-contract` ที่เกี่ยวข้อง

## ขอบเขต

- ฟิลด์และการเชื่อมโหนด → [dify-dsl-nodes](../dify-dsl-nodes/SKILL.md)
- การเลือกเทมเพลตและรูปแบบย่อย → [dify-dsl-templates](../dify-dsl-templates/SKILL.md)
- กลยุทธ์ตรวจ แก้ไข และปรับปรุง → [dify-dsl-quality](../dify-dsl-quality/SKILL.md)
- การเผยแพร่ ความครอบคลุม และผลกระทบ → [dify-dsl-governance](../dify-dsl-governance/SKILL.md)

## เวอร์ชันผลลัพธ์ใหม่

อ่าน [ข้อกำหนดเวอร์ชัน](references/dsl-version-policy.th.md) ก่อนสร้าง DSL ใช้ `version: '0.7.0'` สำหรับ `kind: app` และ `version: '0.1.0'` สำหรับ `kind: rag_pipeline` อย่าคัดลอก header เก่าจาก fixtures หรือ replay
