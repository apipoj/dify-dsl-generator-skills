# ตัวอย่างทีม Research → Writing → Review

[ดาวน์โหลดไฟล์ YAML](../examples/research-writing-review-th-0.7.0.yml) · [คู่มือทั้งหมด](README.md)

ตัวอย่างนี้เป็น Dify Workflow ที่มี **Classic Agent nodes 3 ตัว** ทำงานตามลำดับ ใช้ Function Calling เพื่อค้นหลักฐาน เขียนบทความภาษาไทย และตรวจแก้ก่อนส่งผลลัพธ์ เป็นการจัดเส้นทางคงที่ใน workflow ไม่ใช่การสร้าง subagent เพิ่มเองระหว่างทำงาน

เลือก Classic Agent เพราะอยู่ในขอบเขตที่ชุดทักษะนี้รองรับ และไม่ต้องเตรียม Agent v2 packages หรือผูก published agent ของ workspace ใช้ `kind: app`, `app.mode: workflow`, `version: '0.7.0'`

## โครงสร้างและการส่งข้อมูล

```mermaid
flowchart LR
    S[หัวข้อและกลุ่มผู้อ่าน] --> R[Research: ค้นหลักฐาน]
    R --> W[Writing: เขียนร่าง]
    W --> V[Review: ตรวจและปรับปรุง]
    V --> E[ผลลัพธ์พร้อมหลักฐาน]
```

| โหนด | รับข้อมูล | หน้าที่และเครื่องมือ | ข้อมูลออก |
| --- | --- | --- | --- |
| `start` | `topic`, `audience` | รับหัวข้อและกลุ่มผู้อ่าน | ตัวแปรโจทย์ |
| `research` | โจทย์ | ค้นด้วย DuckDuckGo จัดบันทึกพร้อม source ID และ URL | `text` เป็นบันทึกวิจัย |
| `writing` | โจทย์และ `research.text` | เขียนจากหลักฐานที่ได้รับ ไม่มีเครื่องมือค้นเว็บ | `text` เป็นร่างแรก |
| `review` | โจทย์ บันทึกวิจัย และร่างแรก | ตรวจข้อกล่าวอ้าง ภาษา และอ้างอิง ค้นซ้ำได้ด้วย DuckDuckGo | `text` เป็นฉบับปรับปรุงพร้อมบันทึกตรวจ |
| `end` | ผลของทั้งสามบทบาท | ส่งผลลัพธ์สามฟิลด์ | `final_document`, `research_notes`, `first_draft` |

เส้นเชื่อมหลักมี 4 เส้น: `start → research → writing → review → end` ส่วนข้อมูลวิจัยส่งให้ reviewer ด้วย selector โดยตรง เพราะอยู่ต้นทางเดียวกัน ไม่ต้องคัดลอกผ่าน writer

## เตรียม Dify ก่อนนำเข้า

1. ใช้ Dify ที่รองรับ App DSL `0.7.0` และ Classic Agent node พร้อม plugin runtime
2. ติดตั้งปลั๊กอิน **Dify Agent Strategies**, **OpenAI** และ **DuckDuckGo** จากแหล่งที่ workspace อนุญาต
3. ตั้งค่า credential ของโมเดลใน Dify ตัวอย่างเลือก `langgenius/openai/openai` / `gpt-4o-mini` เป็นค่าเริ่มต้น หากใช้โมเดลอื่น ให้เปลี่ยน model selector ของ Agent ทั้งสามตัว และเลือกโมเดลที่รองรับ tool calling
4. นำเข้าไฟล์ YAML เป็น Workflow แล้วตรวจ Agent แต่ละตัวก่อนกดรัน

ไฟล์ใช้ `dependencies: []` เพื่อไม่เดาเวอร์ชันหรือ hash ของปลั๊กอินใน marketplace จึง **ไม่ติดตั้งปลั๊กอินให้อัตโนมัติ** ต้องติดตั้งตามรายการข้างต้นก่อน หาก Dify แสดง strategy หรือ tool ว่าไม่พบ ให้เลือก FunctionCalling และ DuckDuckGo Search ใหม่ในโหนดที่เกี่ยวข้อง แล้ว export ไฟล์จาก workspace เพื่อเก็บ dependency ที่ตรงกับเครื่องจริง

ไม่มี API key หรือ credential ID อยู่ในตัวอย่าง ไม่ต้องใส่คีย์ลงใน repository

## เช็กลิสต์ก่อนรัน

| จุดตรวจ | ค่าของตัวอย่าง |
| --- | --- |
| Strategy provider | `langgenius/agent/agent` |
| Strategy | `function_calling` |
| Agent tool parameter version | `tool_node_version: '2'` |
| Model selector | `provider`, `model`, `model_type: llm`, `mode: chat` |
| เครื่องมือค้น | `langgenius/duckduckgo/duckduckgo` / `ddgo_search` |
| Query ของเครื่องมือ | ให้ Agent สร้างค่าเองด้วย `auto: 1` |
| จำนวนผลค้นต่อครั้ง | 5 |
| ขีดจำกัดรอบต่อ Agent | Research 5, Writing 2, Review 4 |
| Prompt และตัวแปร | อ้าง `start.topic`, `start.audience`, `research.text`, `writing.text` |

ขีดจำกัดรอบช่วยจำกัดการทำงาน แต่ยังมีค่าใช้จ่ายและเวลารอจากโมเดลกับเครื่องมือ การเพิ่มจำนวนรอบไม่ได้รับประกันว่าคำตอบถูกต้องขึ้น

## ลองรัน

กรอก:

```text
topic: ประโยชน์และข้อจำกัดของการใช้ RAG กับฐานความรู้ภายในองค์กร
audience: เจ้าของธุรกิจ SME ที่เริ่มนำ AI มาใช้งาน
```

ผลที่ควรตรวจ:

- `research_notes` มีข้อค้นพบพร้อม source ID และ URL ที่ได้จากเครื่องมือจริง ถ้าค้นไม่สำเร็จ ต้องระบุข้อจำกัด
- `first_draft` อ้างอิงตรงกับบันทึกวิจัย และไม่อ้างว่า writer ค้นเว็บเอง
- `final_document` มีบทความฉบับปรับปรุง แหล่งอ้างอิง และบันทึกว่าแก้อะไรหรืออะไรยังยืนยันไม่ได้
- ใน trace ต้องเห็นการเรียก `ddgo_search` ของ Research จริง การเรียกค้นซ้ำของ Review ขึ้นกับประเด็นที่ต้องตรวจ
- ถ้าเอาเครื่องมือหรือ credential ออก workflow อาจหยุดด้วยข้อผิดพลาด ต้องตั้งค่าแล้วรันใหม่ ไม่ถือว่าเป็นผลสำเร็จ

## ขอบเขตคุณภาพและการทดสอบ

Prompt กำหนดให้แยก snippet ออกจากหน้าเต็ม ห้ามแต่ง URL และไม่นำคำสั่งจากเนื้อหาเว็บมาใช้เปลี่ยนบทบาท อย่างไรก็ตาม ข้อกำหนดใน prompt ไม่ใช่ตัวตรวจความจริงหรือระบบป้องกันที่รับประกันผล ต้องตรวจ trace และแหล่งอ้างอิงก่อนนำเนื้อหาไปใช้

DuckDuckGo Search ให้ผลค้น ไม่ใช่เครื่องมืออ่านหน้าเต็มโดยอัตโนมัติ หากต้องการหลักฐานจากบทความฉบับเต็ม ต้องเพิ่มเครื่องมืออ่านเว็บใน workspace และปรับ prompt ตามเครื่องมือที่ติดตั้งจริง

ตรวจไฟล์ในเครื่อง:

```bash
python3 scripts/validate_generated_dsl.py examples/research-writing-review-th-0.7.0.yml
python3 -m unittest discover -s tests -p 'test_*.py'
```

สถานะของตัวอย่าง: ตรวจ YAML, output contract, lint, การเชื่อมกราฟ และ selector ในเครื่องแล้ว ยังไม่ได้ทดสอบนำเข้าหรือรันกับ Dify จริง จึงเป็นตัวอย่างที่ต้องตั้งค่าและทดสอบต่อ ไม่ใช่ไฟล์ที่รับรองว่าใช้ได้ทุกเวอร์ชันหรือทุก workspace

## หลักฐานรูปแบบ Agent

ตรวจผ่าน Exa และ source ต้นทางวันที่ 17 กันยายน 2026:

- [Agent node ของ Dify](https://docs.dify.ai/en/self-host/use-dify/nodes/agent)
- [Function Calling strategy และพารามิเตอร์ที่ต้องมี](https://github.com/langgenius/dify-official-plugins/blob/main/agent-strategies/cot_agent/strategies/function_calling.yaml)
- [การแปลง model selector และ tool parameters ใน runtime](https://github.com/langgenius/dify/blob/main/api/core/workflow/nodes/agent/runtime_support.py)
- [DuckDuckGo Search tool และฟิลด์ตั้งค่า](https://github.com/langgenius/dify-official-plugins/blob/main/tools/duckduckgo/tools/ddgo_search.yaml)
