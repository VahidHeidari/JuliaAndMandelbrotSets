@echo off

cls
del /q /s *.pyc

del /q *.bmp
del /q julia\*.bmp
del /q julia\animated\*.bmp
del /q mandelbrot\*.bmp
del /q mandelbrot\animated\*.bmp

rmdir /q julia\animated
rmdir /q julia
rmdir /q mandelbrot\animated
rmdir /q mandelbrot

