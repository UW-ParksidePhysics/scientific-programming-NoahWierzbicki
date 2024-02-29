#!/bin/sh

chapter_name="functions_and_branching"


mkdir $chapter_name

files="convert_celsius_temperature_to_fahrenheit.py calculate_quadratic_roots.py build_polynomial_from_product.py integrate_by_trapezoids_adaptively.py sum_sines.py calculate_gaussian.py calculate_numerical_derivatives.py calculate_velocity_and_acceleration.py compute_heaviside.py compute_smoothed_heaviside.py calculate_piecewise_constant_function.py sort_stars_data.py"

for file in $files 
do 
	touch $chapter_name/$file 
#	git add $chapter_name/$file 
done
git add $chapter_name/

name=`echo $chapter_name | sed 's/_/ /g'`

git commit –m "Adding empty files for $name"
git push

