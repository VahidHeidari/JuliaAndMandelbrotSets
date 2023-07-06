@echo off

cls
del /q /s *.pyc
del /q *.bmp

del /q julia\*.bmp
rmdir /q julia
del /q mandelbrot\*.bmp
rmdir /q mandelbrot 

