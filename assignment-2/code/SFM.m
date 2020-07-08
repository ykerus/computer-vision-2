function point_set = SFM(pvm, adding_method, outlier_thres, plot)
    
    % TO DO: adjust parameters 
    blocks = get_dense_blocks(pvm, 5, 3, 10);
    
    % All points together.
    point_set = zeros(3,size(pvm,2));
    point_indices = [];
    
    % iterate over all dense blocks
    for block = 1:size(blocks,1)
       n_block = normalize_SFM(blocks(block).d_block);
       
       % Factorizing (Slides 76 and onward)
       [U,W,V] = svd(n_block);
       
       U3 = U(:, 1:3);
       W3 = W(1:3, 1:3).^0.5;
       V3 = V(:, 1:3);
       
       M = U3*W3;
       S = W3*V3';
       
       if plot == true && mod(4, block) == 0
           figure(block);
           plot3(S(1,:), S(2,:), S(3,:), "o");
       end
       
       % If it is the first block, add assign new points 
       if size(point_indices) == 0
           point_set(:, blocks(block).index) = S;
           point_indices = blocks(block).index;
           
       else
           common_idx = intersect(point_indices, blocks(block).index);

           S_idx = [];
           S_x = 1;
           for i = 1:length(common_idx)
               while common_idx(i) ~= blocks(block).index(S_x)
                   S_x = S_x + 1;
               end
               S_idx = [S_idx, S_x];
           end

           [~, Z, t] = procrustes(point_set(:,common_idx)', S(:,S_idx)');
           
           if adding_method == "override"
               point_set(:,common_idx) = Z';
           elseif adding_method == "empty"
               for z_id = 1:size(Z,1)
                   if point_set(1,blocks(block).index(z_id)) == 0
                       point_set(:,blocks(block).index(z_id)) = Z(z_id, :)';
                   end
               end
           end
           point_indices = union(point_indices, blocks(block).index);
           
           
       end

    end
    
    if plot == true
        figure(size(blocks,1)+1);
        title('Final construction')
        means = mean(point_set,2);
        
        idx = [];
        for x = 1:size(point_set,2)
            if sum(abs(point_set(:,x))) < outlier_thres
                idx = [idx; x];
            end
        end
        
        plot3(point_set(1, idx), point_set(2, idx), point_set(3, idx), "o");
        title('Final construction')
    end

end