function [p1, p2] = get_matching_points(I1, I2)
    % https://www.vlfeat.org/overview/sift.html
    
    % INPUT
    % I1 - image 1
    % I2 - image 3
    %
    % OUTPUT
    % x - x coordinates of matching points
    % y - y coordinates of matching points
    
    % vl_sift requires single precision gray scale image.
    I1 = single(I1);
    I2 = single(I2);
    
    [f1, d1] = vl_sift(I1);
    [f2, d2] = vl_sift(I2);
    
    % to do: test filter params
    [matches, scores] = vl_ubcmatch(d1, d2);
    
    p1 = [f1(1:2,matches(1,:));ones(1,size(matches,2))];
    p2 = [f2(1:2,matches(2,:));ones(1,size(matches,2))];
end