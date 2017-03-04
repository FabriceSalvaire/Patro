####################################################################################################

from Valentina.Logging import Basic

####################################################################################################

from pathlib import Path

####################################################################################################

from Valentina.FileFormat.Measurements import VitFile
from Valentina.FileFormat.Pattern import ValFile
from Valentina.Geometry.Vector import Vector2D
from Valentina.Painter.Paper import PaperSize
from Valentina.Painter.TexPainter import TexPainter
from Valentina.Pattern.Pattern import Pattern

####################################################################################################

vit_file = VitFile(Path('patterns', 'measurements.vit'))
measurements = vit_file.measurements

####################################################################################################

pattern = Pattern(measurements, 'cm')

####################################################################################################

pattern.SinglePoint(name='A0', x=0.79375, y=1.05833, label_offset=Vector2D(0.132292, 0.264583))
pattern.EndLinePoint(name='A1', base_point='A0', angle=0, length='waist_circ/2+10', label_offset=Vector2D(0.132292, 0.264583), line_style='dashDotLine', line_color='black')
pattern.NormalPoint(name='A2', first_point='A0', second_point='A1', angle=180, length='leg_waist_side_to_floor+@longeur_ourlet_bas_pantalon', label_offset=Vector2D(0.132292, 0.264583), line_style='dashDotLine', line_color='black')
pattern.AlongLinePoint(name='A3', first_point='A0', second_point='A2', length=4, label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='A4', first_point='A0', second_point='A2', length=20, label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='A5', first_point='A0', second_point='A2', length='leg_waist_side_to_floor-@leg_crotch_to_floor_men', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='A6', first_point='A0', second_point='A2', length='leg_waist_side_to_floor-height_knee', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.NormalPoint(name='A', first_point='A5', second_point='A2', angle=0, length='Line_A0_A1', label_offset=Vector2D(-0.616215, -1.90609), line_style='dashDotLine', line_color='black')
pattern.AlongLinePoint(name='B', first_point='A', second_point='A5', length='hip_circ/8', label_offset=Vector2D(0.278141, 0.118734), line_style='hair', line_color='black')
pattern.AlongLinePoint(name='C', first_point='B', second_point='A5', length='@tour_bassin_avec_aisance_pantalon_plat/4+1.5', label_offset=Vector2D(-0.799275, 1.06307), line_style='hair', line_color='black')
pattern.AlongLinePoint(name='D', first_point='C', second_point='A', length='(Line_A_B+Line_B_C)/2', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='A7', first_point='D', second_point='A', angle=0, length='Line_A0_A5', label_offset=Vector2D(-0.13387, -2.53012), line_style='dashDotLine', line_color='black')
pattern.NormalPoint(name='Ic', first_point='D', second_point='A', angle=180, length='Line_A5_A2', label_offset=Vector2D(0.132292, 0.264583), line_style='dashDotLine', line_color='black')
pattern.NormalPoint(name='A9', first_point='A4', second_point='A2', angle=0, length='Line_A0_A1', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='A10', first_point='A3', second_point='A2', angle=0, length='Line_A0_A1', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='A11', first_point='A6', second_point='A2', angle=0, length='Line_A0_A1', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.PointOfIntersection(name='E', first_point='D', second_point='A3', label_offset=Vector2D(0.132292, 0.264583))
pattern.AlongLinePoint(name='Ep', first_point='E', second_point='A10', length=3.5, label_offset=Vector2D(-1.46468, 1.19615), line_style='none', line_color='black')
pattern.NormalPoint(name='Epp', first_point='Ep', second_point='A10', angle=0, length=3.5, label_offset=Vector2D(1.06386, -0.00157887), line_style='hair', line_color='black')
pattern.NormalPoint(name='Ap', first_point='A', second_point='B', angle=0, length=1, label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.PointOfIntersection(name='Bp', first_point='B', second_point='A4', label_offset=Vector2D(0.664616, -2.6632))
pattern.Line(first_point='Ap', second_point='B', line_style='hair', line_color='black')
pattern.Line(first_point='Epp', second_point='Bp', line_style='hair', line_color='black')
pattern.Line(first_point='Bp', second_point='B', line_style='hair', line_color='black')
pattern.SimpleInteractiveSpline(first_point='Bp', second_point='Ap', angle1=281.664, length1=5.09396, angle2=191.328, length2=6.97496, line_style='solid', line_color='black')
pattern.AlongLinePoint(name='A12', first_point='Bp', second_point='Epp', length=-5, label_offset=Vector2D(2.39467, -1.7956), line_style='none', line_color='black')
pattern.AlongLinePoint(name='F', first_point='Bp', second_point='A4', length='Line_B_C', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.PointOfIntersection(name='G', first_point='F', second_point='A3', label_offset=Vector2D(0.132292, 0.264583))
pattern.Line(first_point='G', second_point='Epp', line_style='hair', line_color='black')
pattern.PointOfIntersection(name='Hc', first_point='D', second_point='A6', label_offset=Vector2D(0.132292, 0.264583))
pattern.AlongLinePoint(name='H', first_point='Hc', second_point='A11', length='(@circ_genou_avec_aisance_pantalon_plat/2+2)/2', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='Hp', first_point='Hc', second_point='A6', length='Line_Hc_H', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='Ip', first_point='Ic', second_point='A2', length='@largeur_bas_pantalon/2+2', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.AlongLinePoint(name='I', first_point='Ip', second_point='Ic', length='2*Line_Ic_Ip', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.Line(first_point='Ip', second_point='Hp', line_style='hair', line_color='black')
pattern.Line(first_point='H', second_point='I', line_style='hair', line_color='black')
pattern.Line(first_point='Hp', second_point='F', line_style='hair', line_color='black')
pattern.Line(first_point='H', second_point='Ap', line_style='hair', line_color='black')
pattern.LineIntersectPoint(name='Cp', point1_line1='F', point2_line1='Hp', point1_line2='C', point2_line2='D', label_offset=Vector2D(0.132292, 0.264583))
pattern.Line(first_point='F', second_point='G', line_style='hair', line_color='black')
pattern.Line(first_point='C', second_point='F', line_style='hair', line_color='black')
pattern.NormalPoint(name='A8', first_point='A0', second_point='A2', angle=180, length='waist_circ/3+10', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='A13', first_point='A3', second_point='A2', angle=180, length='Line_A0_A8', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='A14', first_point='A4', second_point='A2', angle=180, length='Line_A0_A8', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='J', first_point='A5', second_point='A2', angle=180, length='Line_A0_A8', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.NormalPoint(name='A16', first_point='A6', second_point='A2', angle=180, length='Line_A0_A8', label_offset=Vector2D(-3.53934, 1.05468), line_style='hair', line_color='black')
pattern.AlongLinePoint(name='K', first_point='J', second_point='A5', length='hip_circ/4/6', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='L', first_point='K', second_point='A5', length='@tour_bassin_avec_aisance_pantalon_plat/4-1.5', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='M', first_point='L', second_point='K', length='(Line_J_K+Line_K_L)/2', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.NormalPoint(name='A15', first_point='M', second_point='A5', angle=0, length='Line_A0_A5', label_offset=Vector2D(-2.92787, -3.5768), line_style='dashDotLine', line_color='black')
pattern.NormalPoint(name='Oc', first_point='M', second_point='A5', angle=180, length='Line_A5_A2', label_offset=Vector2D(0.132292, 0.264583), line_style='dashDotLine', line_color='black')
pattern.PointOfIntersection(name='Kp', first_point='K', second_point='A13', label_offset=Vector2D(-1.19852, -2.26395))
pattern.PointOfIntersection(name='Lp', first_point='L', second_point='A13', label_offset=Vector2D(1.4631, 1.06307))
pattern.Line(first_point='K', second_point='Kp', line_style='hair', line_color='black')
pattern.Line(first_point='L', second_point='Lp', line_style='hair', line_color='black')
pattern.PointOfIntersection(name='Jp', first_point='K', second_point='A14', label_offset=Vector2D(0.132292, 0.264583))
pattern.AlongLinePoint(name='Kpp', first_point='Kp', second_point='Lp', length=1.5, label_offset=Vector2D(1.33002, -3.3286), line_style='none', line_color='black')
pattern.NormalPoint(name='Jpp', first_point='Kpp', second_point='Kp', angle=0, length=1, label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.Line(first_point='Jpp', second_point='Lp', line_style='hair', line_color='black')
pattern.Line(first_point='Jpp', second_point='Jp', line_style='hair', line_color='black')
pattern.PointOfIntersection(name='Nc', first_point='M', second_point='A16', label_offset=Vector2D(0.132292, 0.264583))
pattern.AlongLinePoint(name='N', first_point='Nc', second_point='A6', length='(@circ_genou_avec_aisance_pantalon_plat/2-2)/2', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='Np', first_point='Nc', second_point='A16', length='Line_Nc_N', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='O', first_point='Oc', second_point='A2', length='@largeur_bas_pantalon/2-2', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.AlongLinePoint(name='Op', first_point='O', second_point='Oc', length='2*Line_Oc_O', label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.Line(first_point='O', second_point='N', line_style='hair', line_color='black')
pattern.Line(first_point='Np', second_point='Op', line_style='hair', line_color='black')
pattern.Line(first_point='N', second_point='L', line_style='hair', line_color='black')
pattern.Line(first_point='Np', second_point='J', line_style='hair', line_color='black')
pattern.SimpleInteractiveSpline(first_point='Jp', second_point='J', angle1=263.477, length1=3.00826, angle2=16.7987, length2=3.33672, line_style='solid', line_color='black')
pattern.AlongLinePoint(name='A18', first_point='Jp', second_point='Jpp', length=-2, label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.SimpleInteractiveSpline(first_point='G', second_point='Cp', angle1=257.56, length1=5.44891, angle2=104.852, length2=4.65731, line_style='solid', line_color='black')
pattern.AlongLinePoint(name='A17', first_point='H', second_point='Ap', length='CurrentLength/2', label_offset=Vector2D(0.132292, 0.264583), line_style='none', line_color='black')
pattern.NormalPoint(name='A19', first_point='A17', second_point='H', angle=0, length=-0.75, label_offset=Vector2D(-5.05884, -1.99659), line_style='hair', line_color='black')
pattern.Line(first_point='Ap', second_point='A19', line_style='dotLine', line_color='black')
pattern.Line(first_point='A19', second_point='H', line_style='dotLine', line_color='black')
pattern.SimpleInteractiveSpline(first_point='Ap', second_point='H', angle1=251.913, length1=8.85757, angle2=85.3921, length2=8.65783, line_style='solid', line_color='black')
pattern.SimpleInteractiveSpline(first_point='J', second_point='Np', angle1=280.053, length1=8.13218, angle2=89.1153, length2=7.49977, line_style='solid', line_color='black')
pattern.AlongLinePoint(name='A20', first_point='J', second_point='Np', length='CurrentLength/2', label_offset=Vector2D(-4.46887, 1.14763), line_style='none', line_color='black')
pattern.NormalPoint(name='A21', first_point='A20', second_point='Np', angle=0, length=0.5, label_offset=Vector2D(1.34068, -2.29162), line_style='hair', line_color='black')
pattern.Line(first_point='J', second_point='A21', line_style='dotLine', line_color='black')
pattern.Line(first_point='A21', second_point='Np', line_style='dotLine', line_color='black')
pattern.AlongLinePoint(name='A22', first_point='Lp', second_point='L', length='CurrentLength/2', label_offset=Vector2D(-5.53783, -0.33961), line_style='none', line_color='black')
pattern.NormalPoint(name='A23', first_point='A22', second_point='L', angle=0, length=0.5, label_offset=Vector2D(1.61954, -1.36209), line_style='hair', line_color='black')
pattern.Line(first_point='Lp', second_point='A23', line_style='dotLine', line_color='black')
pattern.Line(first_point='A23', second_point='L', line_style='dotLine', line_color='black')
pattern.SimpleInteractiveSpline(first_point='Lp', second_point='L', angle1=277.265, length1=7.09871, angle2=83.7749, length2=5.44189, line_style='solid', line_color='black')
pattern.AlongLinePoint(name='A24', first_point='G', second_point='Epp', length='CurrentLength/3', label_offset=Vector2D(-0.979432, -2.09783), line_style='none', line_color='black')
pattern.NormalPoint(name='A25', first_point='A24', second_point='G', angle=0, length=8, label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.AlongLinePoint(name='A26', first_point='A24', second_point='G', length=2, label_offset=Vector2D(-1.74375, 2.2101), line_style='none', line_color='black')
pattern.AlongLinePoint(name='A27', first_point='A24', second_point='Epp', length='Line_A24_A26', label_offset=Vector2D(2.70315, 0.681479), line_style='none', line_color='black')
pattern.Line(first_point='A26', second_point='A25', line_style='hair', line_color='black')
pattern.Line(first_point='A25', second_point='A27', line_style='hair', line_color='black')
pattern.AlongLinePoint(name='A30', first_point='Lp', second_point='Jpp', length='CurrentLength/3', label_offset=Vector2D(1.57744, 4.19639), line_style='none', line_color='black')
pattern.NormalPoint(name='A31', first_point='A30', second_point='Lp', angle=0, length=-8, label_offset=Vector2D(0.132292, 0.264583), line_style='hair', line_color='black')
pattern.AlongLinePoint(name='A32', first_point='A30', second_point='Lp', length=2, label_offset=Vector2D(1.00137, 0.681109), line_style='none', line_color='black')
pattern.AlongLinePoint(name='A33', first_point='A30', second_point='Jpp', length='Line_A30_A32', label_offset=Vector2D(-4.2484, 1.01162), line_style='none', line_color='black')
pattern.Line(first_point='A33', second_point='A31', line_style='hair', line_color='black')
pattern.Line(first_point='A32', second_point='A31', line_style='hair', line_color='black')
pattern.NormalPoint(name='A36', first_point='A30', second_point='Lp', angle=0, length=0.5, label_offset=Vector2D(-1.57131, -4.18524), line_style='hair', line_color='black')
pattern.SimpleInteractiveSpline(first_point='Jpp', second_point='A36', angle1=351.01, length1=4.80599, angle2=206.303, length2=2.25922, line_style='solid', line_color='black')
pattern.SimpleInteractiveSpline(first_point='A36', second_point='Lp', angle1=348.354, length1=3.98636, angle2=191.067, length2=3.54739, line_style='solid', line_color='black')

####################################################################################################

pattern.dump()

pattern.eval()

output = Path('output')
output.mkdir(exist_ok=True)

scene = pattern.detail_scene()

tex_path = output.joinpath('pattern-from-api-a0.tex')
paper = PaperSize('a0', 'portrait', 10)
tex_painter = TexPainter(str(tex_path), scene, paper)
tex_painter.add_detail_figure()
tex_painter._document.write()

tex_path = output.joinpath('pattern-from-api-a4.tex')
paper = PaperSize('a4', 'portrait', 10)
tex_painter = TexPainter(str(tex_path), scene, paper)
tex_painter.add_tiled_detail_figure()
tex_painter._document.write()

# Fixme:
val_file = ValFile()
val_file.Write(output.joinpath('write-test-from-api.val'), vit_file, pattern)
