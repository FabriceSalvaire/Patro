####################################################################################################

from Patro.Measurement import MeasurementSet
### from Patro.GraphicEngine.Sketch import Sketch

####################################################################################################

M = MeasurementSet()
# M.add(name, value, full_name description)
M.add('large_hip', 100)
# or M.add('large hip', 100)
M.add('waist_to_large_hip_length', 22)

# ???
# M['large hip'] = 100
# M.large_hip = 100

print(M.dump())
print(M.large_hip)

####################################################################################################

#### # Construction Frame
#### sketch = Sketch('lingerie basic bodice', measurements=M)
#### 
#### hip_line = sketch.hline()
#### # hip_line = sketch.hline(at=sketch.origin)
#### 
#### # Drawing the large hipline
#### 
#### A = hip_line.point()
#### # A = hip_line.point(distance=0)
#### 
#### B = hip_line.point(distance=M.large_hip / 2 + 3, at=A)
#### # B = hip_line.point(distance='large_hip/2 + 3')
#### # from_
#### 
#### back_center_axe = A.vline(trim_before=A)
#### # back_center_axe = sketch.vline(at=A)
#### 
#### front_center_axe = A.vline(trim_before=A)
#### 
#### hip_line.trim(at=A, distance=-2)
#### # hip_line.trim(at=A, distance=2, direction=LEFT)
#### hip_line.trim(at=B, distance=2)
#### # before after
#### 
#### # Drawing the waistline
#### 
#### E = front_center_axe.point(distance=M.waist_to_large_hip_length)
#### F, waist_line = hip_line.parallel(at=E, to=back_center_axe)
#### # F = front_center_axe.perpendicular(at=E, to=back_center_axe)
#### 
#### C = front_center_axe.point(distance=M.center_front_line, at=B)
#### D = back_center_axe.point(distance=M.center_back_line, at=A)
#### # at is explicit
#### 
#### G = front_center_axe.point(at=E, distance=-9)
#### # G = front_center_axe.point(at=E, distance=9, direction=DOWN)
#### H, small_hip_line = hip_line.parallel(at=G, to=back_center_axe)
#### 
#### E1 = waist_line.point(at=E, distance=M.bust_value/2)
#### _ = E1.vline(trim_before=hip_line)
#### P = sketch.constrained_point(from_=C, on=_, distance=M.bust_length, segment=True)
#### I, J, bust_line = hip_line.parallel(at=E, from_=front_center_axe, to=back_center_axe)
#### 
#### L = sketch.middle(D, J)
#### K, body_width_line = hip_line.parallel(at=L, to=front_center_axe)
#### 
#### # Drawing the axis for side seam lines
#### 
#### # On the large hipline
#### A1 = hip_line.point(at=A, distance=M.large_hip/4 -1)
#### B1 = hip_line.point(at=B, distance=M.large_hip/4 +1)
#### 
#### # On the bust line
#### J1 = bust_line.point(at=J, distance=M.full_bust/4)
#### I1 = bust_line.point(at=I, distance=M.full_bust/4, direction=J)
#### A1.segment(J1)
#### B1.segment(I1)
#### # sketch.segment(A1, J1)
#### # sketch.segment(B1, I1)
#### 
#### # Drawing the front neckline
#### C1, _ = front_center_axe.perpendicular(at=C, distance=M.neckline/2/3 + .5, direction=LEFT)
#### C2, _ = _.perpendicular(at=C1, distance=Distance(C, C1))
#### # C2, _ = _.perpendicular(at=C1, distance=C.distance(C1))
#### 
#### # Drawing the front shoulder line
#### C3 = sketch.middle(C1, C2)
#### _ = sketch.vline(at=C3)
#### # waist_line.parallel
#### # _.perpendicular
#### C4 = sketch.constrained_point(from_=C2, on=_, distance=M.shoulder_length, segment=True)
#### 
#### # Drawing the back neckline
#### D1, _ = back_center_axe.perpendicular(at=D, distance=M.neckline/2/3*(1+1/6), direction=LEFT)   # distance ??? 
#### D2, _ = _.perpendicular(at=D1, distance=Distance(D, D1)/3)
#### 
#### # Drawing the back shoulder line
#### L1 = body_width_line.point(at=L, distance=M.cross_back/2, direction=K)
#### _ = back_center_axe.parallel(at=L1)
#### # _ = body_width_line.perpendicular(at=L1)
#### L2 = _.point(at=L1, distance=Distance(D, D1) + 3)
#### L1L2 = _.perpendicular(at=L2)
#### L3 = sketch.constrained_point(from_=D2, on=L1L2, distance=M.shoulder_length + M.shoulder_blase_dart, segment=True)
