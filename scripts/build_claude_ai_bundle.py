#!/usr/bin/env python3
"""Build one self-contained Claude.ai upload, preserving cross-skill paths."""
from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
NAME = 'dify-dsl-th'
ENTRY = '''---
name: dify-dsl-th
description: สร้าง ตรวจสอบ และปรับปรุง Dify Workflow, Chatflow และ RAG Pipeline DSL เป็นภาษาไทย ใช้เมื่อผู้ใช้ขอไฟล์ YAML สำหรับ Dify หรือให้ตรวจแก้ workflow เดิม
---

# Dify DSL ภาษาไทย

เริ่มจาก [using-dify-dsl](skills/using-dify-dsl/SKILL.md) แล้วอ่านเฉพาะ skill และเอกสารอ้างอิงที่ตรงกับงาน ไฟล์ใน `skills/` เป็นเอกสารประกอบภายในแพ็กเกจนี้ ไม่จำเป็นต้องติดตั้งเป็น skill แยก

ตอบภาษาไทยเว้นแต่ผู้ใช้ขอภาษาอื่น คง YAML keys, node ID, selector และชื่อ provider/model ตามรูปแบบทางเทคนิค

DSL ใหม่ชนิด `app` ใช้ `version: '0.7.0'` ส่วน `rag_pipeline` ใช้ `version: '0.1.0'` อ่าน [ข้อกำหนดเวอร์ชัน](skills/dify-dsl-foundations/references/dsl-version-policy.th.md) ก่อนสร้างหรือเปลี่ยนเวอร์ชัน

## การทำงานใน Claude.ai

- รากแพ็กเกจคือโฟลเดอร์ที่มีไฟล์นี้และ `skills/`, `scripts/`, `tests/` ใช้พาธจริงของแพ็กเกจเมื่อต้องรันคำสั่ง ไม่สมมติ working directory
- สคริปต์ตรวจต้องใช้ Python 3.10+ และ Ruby พร้อม YAML library ตรวจว่ามีเครื่องมือก่อนรัน หากไม่มี ให้ตรวจจากเอกสารและระบุว่ายังไม่ได้ตรวจด้วยสคริปต์ อย่าอ้างว่าได้รันแล้ว
- ตรวจ DSL ที่สร้างด้วย `python3 scripts/validate_generated_dsl.py /absolute/path/output.yml` จากรากแพ็กเกจ คำสั่งนี้ตรวจเวอร์ชันและ lint ไม่ได้ทดสอบบน Dify จริง
- เมื่อต้องใช้ subagent ให้ตรวจว่ามีเครื่องมือและได้รับอนุญาตจริง หากไม่มี ใช้โหมดไม่มี subagent และแจ้งว่ายังไม่ได้ตรวจโดยผู้ตรวจอิสระ ห้ามจำลองหลายบทบาทแล้วอ้างว่าเป็นผู้ตรวจแยกกัน
- สร้างไฟล์ `.yml` ให้ดาวน์โหลดเมื่อมีเครื่องมือสร้างไฟล์ หากไม่มี ให้แสดง YAML ใน code block พร้อมชื่อไฟล์ที่แนะนำ
- การสร้างไฟล์ไม่ใช่การนำเข้าหรือเผยแพร่ไปยัง Dify บอกส่วนที่ยังต้องกำหนด เช่น provider, model, credentials และ dataset ตามจริง
'''


def package_files() -> dict[str, bytes]:
    files = {'SKILL.md': ENTRY.encode('utf-8')}
    for folder in ('skills', 'scripts', 'tests', 'docs', 'examples'):
        for path in sorted((ROOT / folder).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix == '.pyc' or path.name == '.DS_Store':
                continue
            files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    for name in ('LICENSE', 'README.md', 'README.zh-CN.md', 'README.th.md'):
        files[name] = (ROOT / name).read_bytes()
    # These files are referenced by the README; preserve them in the package.
    for name in ('.codex/INSTALL.md', '.codex/INSTALL.th.md', '.claude/INSTALL.th.md', '.github/workflows/validate.yml'):
        files[name] = (ROOT / name).read_bytes()
    return files


def build(output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
        for name, data in sorted(package_files().items()):
            entry = ZipInfo(f'{NAME}/{name}', date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist' / f'{NAME}.zip')
    args = parser.parse_args()
    print(build(args.output.expanduser().resolve()))


if __name__ == '__main__':
    main()
