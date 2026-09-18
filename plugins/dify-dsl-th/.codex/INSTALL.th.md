# ติดตั้งสำหรับ Codex

ติดตั้งแบบ native plugin: [Codex และ Claude Code plugins](../docs/plugins.th.md)


จากราก repository รัน:

```bash
bash scripts/install_codex_bundle.sh
```

สคริปต์สร้าง `~/.agents/skills/dify-dsl` ให้ชี้ไปยัง `skills/` ของ clone นี้ และลบเฉพาะลิงก์เก่าใน `~/.codex/skills/` ที่ชี้ไปยัง skill ของ clone เดียวกัน ไม่แก้ skill จากที่อื่น

เรียก `$using-dify-dsl` ตามด้วยโจทย์ภาษาไทย หาก skill ยังไม่ปรากฏ ให้เริ่มเซสชันหรือเปิด Codex ใหม่ ข้อมูลอาจแสดงทั้งทางเข้าหลักและ skill ย่อยทั้งชุดได้

แก้เนื้อหาที่ `skills/` ได้โดยตรงเพราะเป็น symlink ต้องเก็บ clone นี้ไว้ หากจะย้าย ให้จัดลิงก์ใหม่ให้ตรงกับพาธใหม่

สำหรับ Claude Code และ Claude.ai ให้ใช้ [คู่มือติดตั้ง Claude](../.claude/INSTALL.th.md)
