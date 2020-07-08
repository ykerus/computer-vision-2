function blocks = get_dense_blocks(pvm, max_views_per_block, min_views_per_block, min_points_per_block)

    view_size = size(pvm, 1);
    cur = 1;
    
    blocks = [];
    while cur < view_size
        
        % Always start at x
        if mod(cur ,2)==0
            cur= cur + 1;
        end
        
        next = cur;
        common_points = find(pvm(cur,:));


        while next < view_size
            next = next + 1;
            new_points = find(pvm(next,:));
            matches = intersect(common_points, new_points);
            
            % if the matches are the same as the previous common points, do
            % nothing.
            if next - cur > max_views_per_block 
                blocks = [blocks; new_dense(cur, next, common_points, pvm)];
                break;
            
            % Stop of max number of views is reached
            elseif size(matches,2) == size(common_points,2)              
                continue
            
            % Check whether the matches are still the minimum number of
            % points.
            elseif next - cur < min_views_per_block
                if size(matches,2) < min_points_per_block
                    blocks = [block; new_dense(cur, next, common_points, pvm)];
                    break;
                else
                    common_points = matches;
                end
                
            else
                blocks = [blocks; new_dense(cur, next, common_points, pvm)];
                break;
            end    
        end
        cur = next;
        
    end
    
    function stru = new_dense(cur, next, common_points, pvm)
        if mod(next ,2)~=0
            next = next - 1;
        end
        stru = struct;
        stru.begin_view = cur;
        stru.last_view = next;
        stru.index = common_points;
        stru.d_block = pvm(cur:next, common_points);
    end
    
end