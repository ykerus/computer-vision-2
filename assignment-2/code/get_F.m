function [F,p1,p2] = get_F(I1, I2, method)
    % following variables could be made function args
    sampson_thresh = 1; % inlier threshold
    RANSAC_N = 500; % number of iterations for RANSAC

    [p1, p2] = get_matching_points(I1, I2);

    if method == "standard"
        % feed the non-normalized points to the eight-point algorithm
        F = eight_point_alg(p1, p2);
        
    elseif method == "normalized"
        % feed the normalized points to the eight-point algorithm
        [p1n, T1] = normalize_points(p1);
        [p2n, T2] = normalize_points(p2);
        F = eight_point_alg(p1n, p2n);
        % denormalize F
        F = T2' * F * T1;
        
    elseif method == "RANSAC"
        [p1n, T1] = normalize_points(p1);
        [p2n, T2] = normalize_points(p2);
        
        most_inliers = [];
        
        for i = 1:RANSAC_N
            % take sample of 8 points
            sample = randsample(size(p1,2), 8);
            % use normalized point samples for eight point alg
            F = eight_point_alg(p1n(:,sample), p2n(:,sample));
            F = T2' * F * T1;
            
            % determine num of inliers with sampson distance
            % using the non-normalized points
            d = sampson_dist(p1, p2, F);
            inliers = d < sampson_thresh;
            
            % save the set of inliers if there are more than previous
            if sum(inliers) > sum(most_inliers)
                most_inliers = inliers;
            end 
        end
        % use the full set of inliers to calculate F
        F = eight_point_alg(p1n(:,most_inliers), p2n(:,most_inliers));
        F = T2' * F * T1;
        
        % return inliers 
        p1 = p1(:,most_inliers);
        p2 = p2(:,most_inliers);
        disp("Most number of inliers: "+sum(most_inliers))
      
    end
end