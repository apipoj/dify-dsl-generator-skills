# ติดตั้งสำหรับ Claude Code และ Claude.ai

ติดตั้งแบบ native plugin: [Codex และ Claude Code plugins](../docs/plugins.th.md)


ตรวจสอบแนวทางจากเอกสาร Anthropic วันที่ 17 กันยายน 2026

## Claude Code: ใช้ในโปรเจกต์นี้

จากราก repository รัน:

```bash
python3 scripts/install_claude_code.py
claude
```

จะสร้าง `.claude/skills/<skill-name>` ให้ชี้ไปยัง `skills/<skill-name>` ด้วย relative symlink จึงย้ายหรือ clone repository ได้โดยไม่ผูกกับพาธเครื่องเดิม สคริปต์ตรวจความขัดแย้งครบทุกปลายทางก่อนสร้างลิงก์ และไม่เขียนทับไฟล์หรือ skill อื่น

ใน Claude Code ใช้ `/using-dify-dsl` หรือระบุ skill เฉพาะ เช่น `/dify-dsl-review` ตรวจรายชื่อด้วย `/skills` หากเพิ่งสร้างโฟลเดอร์ skills ระหว่างเปิดเซสชัน ให้เริ่ม Claude Code ใหม่

## Claude Code: ใช้ทุกโปรเจกต์ในเครื่อง

```bash
python3 scripts/install_claude_code.py --user
```

จะสร้างลิงก์ใน `~/.claude/skills/` และอ้างถึง clone นี้ ต้องเก็บ clone ไว้ที่เดิม หรือสร้างลิงก์ใหม่เมื่อย้าย เมื่อเรียกสคริปต์ตรวจจากโปรเจกต์อื่น ให้ใช้พาธจริงของ repository นี้ โดยรากที่มี `skills/` คือฐานของคำสั่งในเอกสาร

สำหรับสภาพแวดล้อมทดสอบหรือพาธอื่น:

```bash
python3 scripts/install_claude_code.py --dest /absolute/path/to/skills
```

## Claude.ai: อัปโหลดชุดเดียว

```bash
python3 scripts/build_claude_ai_bundle.py
```

อัปโหลด `dist/dify-dsl-th.zip` ใน Customize > Skills > เพิ่ม skill > Upload a skill แล้วเปิดใช้งาน บัญชีต้องเปิด Code execution and file creation ตามการตั้งค่าของบัญชีหรือองค์กร

โครงสร้าง ZIP:

```text
dify-dsl-th/
├── SKILL.md
├── skills/        # ทั้ง 12 skill และข้อมูลประกอบ
├── scripts/       # คำสั่งตรวจและจัดแพ็กเกจ
├── tests/         # fixtures และ regression cases
├── docs/
├── examples/
└── LICENSE
```

มีทางเข้าหลักหนึ่งตัวชื่อ `dify-dsl-th` ส่วน skill ย่อยเป็นไฟล์ประกอบที่อ่านเมื่อจำเป็น พาธข้าม skill ยังคงทำงานภายใน ZIP จึงไม่ควรแยก ZIP ออกเป็น 12 ชุด

แพ็กเกจไม่ได้รับประกันว่าทุก runtime จะมี Ruby หรือเครื่องมือ subagent ให้ผู้ช่วยระบุผลตรวจที่ทำได้จริงเสมอ หากไม่มี Ruby ยังอ่านเอกสารและสร้างร่างได้ แต่ต้องตรวจไฟล์ต่อในเครื่องหรือบน Dify ก่อนอ้างว่าพร้อมใช้

## อัปเดตและถอนการติดตั้ง

แก้ไฟล์ใน `skills/` สำหรับ Claude Code แบบ symlink แล้วเปิดเซสชันใหม่หากยังเห็นเนื้อหาเก่า สำหรับ Claude.ai สร้าง ZIP ใหม่และอัปเดต skill ในบัญชี

ถอนการติดตั้ง Claude Code โดยลบเฉพาะ symlink ที่สคริปต์สร้าง ไม่ลบโฟลเดอร์ skills ทั้งหมด ส่วน Claude.ai ปิดหรือลบ `dify-dsl-th` จากรายการ Skills

## แหล่งอ้างอิง

- [Claude Code skill locations และ symlinks](https://code.claude.com/docs/en/skills)
- [สร้าง custom skill และโครงสร้าง ZIP](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [เปิดใช้และอัปโหลด Skills ใน Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
