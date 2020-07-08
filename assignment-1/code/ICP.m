function [baseTF, RMS, Rf, tf, RMSf, time] = ICP(base, target, nb, nt, max_iter, sampling, Npoints, evaluate, print)
    % sampling = {"all", "uniform", "random", "informed"}
    % Npoints is ignored if sampling = "all"
    % nb, nt surface normals
     
    RMS = [];
    
    [baseSmpl, targetSmpl] = samplePcds(base(1:3,:), target(1:3,:), nb, nt, sampling, Npoints);
    bsize = size(baseSmpl, 2);
    tsize = size(targetSmpl, 2);
    baseTF = base;
    
    % save transormations in order to return entire pcd at the end
    rotations = [];
    translations = [];
        
    tic;
    % (1) Initialize R to I (identity matrix) and t = 0.
    R = eye(3);
    t = zeros(3,1);

    % Start iteration.
    for iteration = 1:max_iter
        % (3) Find the closest points for each point 
        % in the base point set (A 1 ) from the target 
        % point set (A 2 ) using brute-force approach.
        
        if sampling == "random" % take new sample
            [baseSmpl, targetSmpl] = samplePcds(baseTF(1:3,:), target(1:3,:), nb, nt, sampling, Npoints);
        end
        matching_points_ids = zeros(bsize,1);
        % Loop over all points in base matrix
        for bi = 1:bsize
            dist_sqrd = zeros(1,tsize);
            % Loop over x, y, z
            for i = 1:3
                % Calculate distances to all target points at once
                dist_sqrd = dist_sqrd + (baseSmpl(i,bi) - targetSmpl(i,:)).^2;
            end
            [~, ti] = min(dist_sqrd);
            matching_points_ids(bi) = ti;
        end
        
        closest_target = targetSmpl(:, matching_points_ids);
        
        if iteration == 1
            rms_score = sqrt(mean(sum((baseSmpl - closest_target).^2, 1)));
            RMS(end+1) = rms_score;
            if print == true
                disp(rms_score)
            end
        end
        
        % (4) Refine R and t using Singular Value Decomposition
        target_mean = mean(closest_target,2);
%         target_mean = mean(unique(closest_target,"rows"),2);
        base_mean = mean(baseSmpl,2);
        
        temp_target = closest_target - target_mean;
        temp_base = baseSmpl - base_mean;

        S = temp_base * temp_target';
        [U, ~, V] = svd(S);
        
        R = V * U';
        
        t = target_mean - R * base_mean;
             
        % (2) Transform the point cloud with R and t.
        
        baseSmpl = (R * baseSmpl) + t; % transform sample
        baseTF(1:3, :) = R * baseTF(1:3, :) + t; % transform entire pcd
        
        rotations = [rotations; R];
        translations = [translations ; t];
         
        % (5) Calculate RMS.
%         rms_score = mean(sqrt(sum(power((baseSmpl - target), 2))));
        rms_score = sqrt(mean(sum((baseSmpl - closest_target).^2, 1)));
        RMS(end+1) = rms_score;
        if print == true
            disp(rms_score)
        end
        if iteration > 2
            r1 = RMS(end-1);
            r2 = RMS(end);
            if abs(r1-r2) < 0.00001
                disp("Stopping early")
                break;
            end
        end
    end
    
    time = toc;
    disp("Elapsed time is " + time + " seconds");
 
    % calculate (general) final transformations R and t
    tf = zeros(3,1);
    Rf = eye(3);
    for i = 0:iteration-1
        idx = i*3+1:i*3+3;
        Rf = rotations(idx,:) * Rf;
        addterm = translations(idx,:);
        for j = i:iteration-2
            idx = idx + 3;
            addterm = rotations(idx, :) * addterm;
        end
        tf = tf + addterm;
    end
    
    % final evaluation on entire pcd
    RMSf = 0;
    if evaluate
        disp("Evaluating on all points...")
        [baseSmpl, targetSmpl] = samplePcds(baseTF(1:3,:), target(1:3,:), nb, nt, "all", 0);
        matching_points_ids = zeros(size(baseSmpl,2),1);
        for bi = 1:size(baseSmpl,2)
            dist_sqrd = zeros(1,size(targetSmpl,2));
            for i = 1:3
                dist_sqrd = dist_sqrd + (baseSmpl(i,bi) - targetSmpl(i,:)).^2;
            end
            [~, ti] = min(dist_sqrd);
            matching_points_ids(bi) = ti;
        end
        closest_target = targetSmpl(:, matching_points_ids);
        RMSf = sqrt(mean(sum((baseSmpl - closest_target).^2, 1)));       
        disp("Final RMS: " + RMSf)
    end
    printRMS(RMS)
end