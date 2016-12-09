
`right_back_up` --> out2
`right_back_down` --> out1
`left_back_up` --> out3
`left_back_down` --> out4

|方向|IN1|IN2|IN3|IN4|
|---|---|---|---|----|
|前进|0| 1 |1 |0 |
|停止| 0| 0| 0| 0| 
|后退| 1| 0| 0| 1 |
|左前转弯| 0 |1 |0| 0 |
|右前转弯|0 |0| 1| 0| 
|左后转弯|1 |0| 0| 0| 
|右后转弯| 0 |0 |0 |1|

```python
    # 下面的相当于是二驱的模式进行控制
    def forward(self): self.exec_operation(self, 0b01100110) 
    def back(self): self.exec_operation(self, 0b10011001)
    def stop(self): self.exec_operation(self, 0b00000000)
    def front_left(self): self.exec_operation(self, 0b00100010)
    def front_right(self): self.exec_operation(self, 0b01000100)
    def back_left(self): self.exec_operation(self, 0b00010001)
    def back_right(self): self.exec_operation(self, 0b10001000)
```
[0b01100110,0b10011001,0b00000000,0b00100010,0b01000100,0b00010001,0b10001000]
对应的十进制：
[102, 153, 0, 34, 68, 17, 136]
制定了这样的对应标准以后，就不需要再写复杂的单个的函数了。

执行时间的长度决定了不同的角度？？由这个问题来看，肯定需要做一个完全的转弯的方向，转动的角度问题还需要计算。

实际上还有更多方向？如果后驱不转动，只前驱转动，实际上拐弯角度更大？
