
method = "RANSAC"; %choose which eight-point algorithm approach
sample = true;     %choose whether the epilines should be sampled or not


folder = "Data/House/House";
I1 = get_house_frame(folder, 1);
I2 = get_house_frame(folder, 2);

[F, p1, p2] = get_F(I1, I2, method);
draw_lines(I1, I2, p1, p2, F, sample)
suptitle("Epilines for subsequent images")