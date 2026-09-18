---
name: dify-dsl-review
description: ตรวจ Dify Workflow, Chatflow หรือ RAG Pipeline DSL แบบอ่านอย่างเดียว เพื่อวิเคราะห์โหมด โครงสร้าง ความเสี่ยง การนำเข้า และความพร้อมเผยแพร่ หากต้องแก้ไฟล์ให้ใช้ refactor หากเป้าหมายยังไม่ชัดให้ใช้ brainstorming
---

# dify-dsl-review

ตรวจแบบอ่านอย่างเดียว ไม่แก้ไฟล์และไม่เขียน DSL ใหม่

## ลำดับการทำงาน

1. อ่าน [dify-dsl-foundations](../dify-dsl-foundations/SKILL.md)
2. เมื่อต้องตรวจโหนดเฉพาะ อ่าน [dify-dsl-nodes](../dify-dsl-nodes/SKILL.md)
3. เมื่อต้องค้นหาและจัดระดับปัญหา ตรวจอิสระ หรือประเมินการปรับปรุง อ่าน [dify-dsl-quality](../dify-dsl-quality/SKILL.md)
4. เมื่อต้องสรุปการเผยแพร่ ความครอบคลุม ผลกระทบ หรือการติดตามระบบ อ่าน [dify-dsl-governance](../dify-dsl-governance/SKILL.md)
5. เมื่อผู้ใช้ขอผู้ตรวจอิสระหลายฝ่าย หรือความซับซ้อนต้องการการตรวจอย่างเป็นระบบ ใช้ [dify-dsl-subagent-review](../dify-dsl-subagent-review/SKILL.md) ตามเครื่องมือและสิทธิ์ที่มี

## ผลลัพธ์ขั้นต่ำ

ระบุโหมด รายการโหนด รายการเส้นเชื่อม เช็กลิสต์ฟิลด์ ระดับความเสี่ยง และข้อสรุป

## ข้อกำหนด

ห้ามแก้ไฟล์หรือเปลี่ยนคำแนะนำให้เป็น DSL ฉบับเขียนใหม่ ถ้าผู้ใช้ขอแผนแก้ขั้นต่ำหรือให้แก้จริง ใช้ [dify-dsl-refactor](../dify-dsl-refactor/SKILL.md) ถ้าเป้าหมายไม่ชัดหรือขอบเขตขัดกัน กลับไป [dify-dsl-brainstorming](../dify-dsl-brainstorming/SKILL.md)
