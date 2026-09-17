---
name: dify-dsl-quality
description: ตรวจคุณภาพ Dify DSL เพื่อค้นหาและจัดระดับปัญหา เลือกวิธีแก้ไขหรือปรับปรุง แบ่งบทบาทผู้ตรวจอิสระ และจัดรายงาน ใช้ในขั้นตรวจ แก้ไข หรือปรับประสิทธิภาพ
---

# dify-dsl-quality

กำหนดวิธีค้นหาปัญหา แก้ไข ตรวจทาน และตรวจอิสระ ไม่แทนการเลือกโหมดหรือข้อสรุปความพร้อมเผยแพร่

## เริ่มอ่าน

อ่าน [ดัชนีอ้างอิง](references/index.md) เมื่อต้องแบ่งบทบาท จึงอ่าน [บทบาทผู้ตรวจ](agents/index.md)

ถ้าต้องจัดการการตรวจด้วย subagent จริง ให้ใช้ [dify-dsl-subagent-review](../dify-dsl-subagent-review/SKILL.md)

เมื่อต้องตรวจด้วยกฎแน่นอน ให้เรียก `scripts/lint_dsl.py` จากโฟลเดอร์ skill นี้ หรือใช้พาธเต็ม ตรวจข้อผิดพลาดของ selector, edge, โหนดปลายทางตามโหมด จุดเริ่ม container และฟิลด์สำคัญก่อนตรวจรายละเอียดต่อ

## ขอบเขต

- โหมดและรูปแบบฟิลด์ยังไม่ชัด → [dify-dsl-foundations](../dify-dsl-foundations/SKILL.md)
- ความพร้อมเผยแพร่ ความครอบคลุม หรือฟิลด์สำหรับติดตามระบบ → [dify-dsl-governance](../dify-dsl-governance/SKILL.md)
- การประเมิน skill ด้วยตัวอย่างจริง → [dify-dsl-forward-testing](../dify-dsl-forward-testing/SKILL.md)
