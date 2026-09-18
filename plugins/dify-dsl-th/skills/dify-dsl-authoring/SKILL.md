---
name: dify-dsl-authoring
description: สร้างร่าง Dify Workflow, Chatflow หรือ RAG Pipeline DSL จากความต้องการที่ชัดเจน ใช้เลือกโหมด เทมเพลต โหนด และเติมฟิลด์ หากยังมีประเด็นที่ขัดขวางการออกแบบ ให้กลับไป dify-dsl-brainstorming
---

# dify-dsl-authoring

เปลี่ยนเป้าหมายที่ชัดเจนเป็นร่าง DSL ไม่ใช่การรับรองว่าพร้อมเผยแพร่

## เงื่อนไขเริ่มงาน

เป้าหมายชัดเจนและเป็นการสร้าง DSL ใหม่หรือสร้างจากเทมเพลต หากผ่าน brainstorming แล้ว ต้องเคลียร์ประเด็นที่ขัดขวางงานก่อน หากยังไม่พร้อม ให้กลับไป [dify-dsl-brainstorming](../dify-dsl-brainstorming/SKILL.md)

## ลำดับการทำงาน

1. อ่าน [dify-dsl-foundations](../dify-dsl-foundations/SKILL.md) เพื่อเลือกโหมด กำหนดฟิลด์ และรูปแบบผลลัพธ์
2. เมื่อต้องเริ่มจากเทมเพลต อ่าน [dify-dsl-templates](../dify-dsl-templates/SKILL.md)
3. เมื่อต้องเลือกและเชื่อมโหนด อ่าน [dify-dsl-nodes](../dify-dsl-nodes/SKILL.md)
4. ถ้าผู้ใช้ขอการตรวจอิสระหลังสร้าง หรือความเสี่ยงสูงจนจำเป็นต้องจัดการการตรวจอย่างเป็นระบบ ให้ใช้ [dify-dsl-subagent-review](../dify-dsl-subagent-review/SKILL.md) ภายใต้เครื่องมือและสิทธิ์ที่มี

## ผลลัพธ์ขั้นต่ำ

ระบุโหมด เทมเพลตที่เลือกและเหตุผลที่ไม่เลือกตัวอื่นถ้ามี รายการโหนด รายการเส้นเชื่อม เช็กลิสต์ฟิลด์ ร่าง DSL และสิ่งที่ยังต้องยืนยัน ถ้างานซับซ้อนหรือเสี่ยงสูง ให้ระบุว่าควรตรวจต่อด้วย subagent-review หรือไม่

## ข้อกำหนด

อย่าฝืนเขียน DSL เมื่อโจทย์ยังคลุมเครือ อย่าข้ามการเลือกโหมด และอย่าอ้างว่านำเข้าได้ทันทีหรือผ่านการตรวจครบถ้วน หากต้องการข้อสรุปนั้น ให้ใช้ [dify-dsl-review](../dify-dsl-review/SKILL.md)

## เวอร์ชันผลลัพธ์ใหม่

อ่าน [ข้อกำหนดเวอร์ชัน](../dify-dsl-foundations/references/dsl-version-policy.th.md) ก่อนสร้าง DSL ใช้ `version: '0.7.0'` สำหรับ `kind: app` และ `version: '0.1.0'` สำหรับ `kind: rag_pipeline` อย่าคัดลอก header เก่าจาก fixtures หรือ replay
