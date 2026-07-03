%TEST1
N10 G54 G20 G90
N20 G00 x0 y0 z5
N21 G90.1 ; esto configura que los centros de los círculos sean absolutos
N30 M03 S1500
N40 G01 z-0.5
( Curva de abajo a la izquierda)
N50 G00 x0.6854 y25.191
N60 G03 x35.8494 y8.1645 I20 J20
( Curva Externa abajo )
N70 G02 x76.4191 y21.7944 I66.36 J-14.85
( Panza inferior del círculo central )
N80 G03 x104.5302 y22.7648 I89 J65
( Recta Tangente abajo a la derecha )
N90 G01 x171.5772 y46.1124 F2000
( Curva de la derecha )
N100 G03 x171.5772 y83.8876 I165 J65 F1200
(Recta tangente de arriba a la derecha )
N110 G01 x104.5302 y107.2352 F2000
( Panza superior del círculo central )
N120 G03 x70.1459 y105.8598 I89 J65 F1200
( Círculo tangente que conecta al centro con la punta )
N130 G03 x0.6854 y25.191 I115.2211 J-3.1917
N140 G00 z5
( Círculo de abajo a la izquierda)
N150 G00 x24 y20
N160 G01 z-0.5
N170 G03 x16 y20 J20 I20
N180 G03 x24 y20 J20 I20
( Círculo del medio )
N190 G00 z5
N200 G00 x127 y65 F2000
N210 G01 z-0.5
N220 G03 x51 y65 I89 J65 F1200
N230 G03 x127 y65 I89 J65
( Pentágono central )
N240 G00 z5
N250 G00 x83.18 y86.73
N260 G01 z-0.5
N270 G01 x104.91 y80.91 F2000
N280 x110.73 y59.18
N290 x94.82 y43.27
N300 x73.09 y49.09
N310 x67.27 y70.82
N320 x83.18 y86.73
( Círculo de la derecha )
N320 G00 z5
N330 x169 y65 F2000
N340 G01 z-0.5
N350 G03 x161 y65 I165 J65 F1200
N360 G03 x169 y65 I165 J65
N370 M05
N380 G00 z5
N390 G00 x0 y0
N400 M30
