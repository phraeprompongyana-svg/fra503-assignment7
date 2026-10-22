# FRA503 Assignment 7: Nav2 และการทดสอบเส้นตรงของ TurtleBot3 Burger

ทดสอบการเคลื่อนที่เส้นตรงของ TurtleBot3 Burger ในสนามสี่เหลี่ยมที่ไม่มีสิ่งกีดขวาง
(ROS 2 Jazzy ใน Docker, บันทึกข้อมูลด้วย ros2 bag รูปแบบ .mcap)

## โครงสร้าง
- `scripts/run_straight.py` สคริปต์สั่งหุ่นยนต์วิ่งตรงด้วยความเร็วคงที่
- `data/maps/` แผนที่ Map4 ที่สร้างด้วย Cartographer (Map4.pgm, Map4.yaml)
- `data/` ไฟล์ bag ของการทดลอง (เฉพาะไฟล์ขนาดไม่เกิน 50 MB)

## วิธีรัน run_straight.py
    python3 scripts/run_straight.py <ความเร็ว m/s> <stamped|twist> [ระยะ m]
    ตัวอย่าง: python3 scripts/run_straight.py 0.06 stamped 1.2

สคริปต์ publish /cmd_vel (TwistStamped บน Jazzy) ที่ 20 Hz และอ่าน /odom
เมื่อระยะถึงเป้าจะส่งคำสั่งหยุดแล้วพิมพ์ระยะสุดท้ายตาม odom

## การทดลอง
- ความเร็ว: 0.03, 0.06, 0.09, 0.12 m/s ไปเป้าหมาย 120 cm (5 รอบต่อความเร็ว)
- ระยะทาง: 25, 50, 100, 120 cm ที่ 0.06 m/s (5 รอบต่อระยะ)
- Nav2: ส่งเป้าหมายเส้นตรง ≈ 1.2 m บนแผนที่ Map4

## ไฟล์ขนาดใหญ่
ไฟล์ bag ที่ใหญ่กว่า 50 MB ไม่ได้อยู่ใน repo นี้ (https://drive.google.com/drive/folders/1usYN1TF2PbsDmspErDNzOA6uo_mvwgg2?usp=sharing)
