#!/usr/bin/env python3
import sys, math, time, rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TwistStamped

V = float(sys.argv[1])
MODE = sys.argv[2]            # stamped หรือ twist
DIST = float(sys.argv[3]) if len(sys.argv) > 3 else 1.2

class Run(Node):
    def __init__(self):
        super().__init__('run_straight')
        self.stamped = (MODE == 'stamped')
        self.pub = self.create_publisher(TwistStamped if self.stamped else Twist, '/cmd_vel', 10)
        self.create_subscription(Odometry, '/odom', self.cb, 10)
        self.p0 = None
        self.d = 0.0
        self.vmax = 0.0
        self.t0 = time.time()
        self.done = False
        self.create_timer(0.05, self.tick)

    def cb(self, m):
        p = m.pose.pose.position
        if self.p0 is None:
            self.p0 = (p.x, p.y)
        self.d = math.hypot(p.x - self.p0[0], p.y - self.p0[1])
        self.vmax = max(self.vmax, m.twist.twist.linear.x)

    def send(self, v):
        if self.stamped:
            m = TwistStamped()
            m.header.stamp = self.get_clock().now().to_msg()
            m.twist.linear.x = v
        else:
            m = Twist()
            m.linear.x = v
        self.pub.publish(m)

    def tick(self):
        if self.p0 is None:
            if time.time() - self.t0 > 5:
                self.get_logger().error('ไม่ได้รับ /odom')
                self.done = True
            return
        if self.d >= DIST or time.time() - self.t0 > 120:
            self.done = True
        else:
            self.send(V)

rclpy.init()
n = Run()
while rclpy.ok() and not n.done:
    rclpy.spin_once(n, timeout_sec=0.1)
for _ in range(20):
    n.send(0.0)
    time.sleep(0.05)
end = time.time() + 2.0        # รอให้หุ่นหยุดนิ่ง
while time.time() < end:
    rclpy.spin_once(n, timeout_sec=0.1)
print(f'สั่ง V={V}  odom ระยะสุดท้าย={n.d*100:.1f} cm  ความเร็วสูงสุดที่ odom วัดได้={n.vmax:.3f} m/s')
n.destroy_node()
rclpy.shutdown()
