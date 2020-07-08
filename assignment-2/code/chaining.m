function pvm = chaining(frames_absent, plot)
% frames_absent = the allowed number of number of frames a point is absent 
% frames_absent = 20 is a good choice (the example PVM.txt shows for 0)
% plot = [true, false]
    thresh = .1; %distance threshold to count point as "the same"
    
    pvm = [];
    %iterate over all frames
    for i = 1:49
        if i == 49
            Ia = get_house_frame("Data/House/House", i);
            Ib = get_house_frame("Data/House/House", 1);
        else
            Ia = get_house_frame("Data/House/House", i);
            Ib = get_house_frame("Data/House/House", i+1);
        end
        [pa, pb] = get_matching_points(Ia, Ib);
        [pa_n, ~] = normalize_points(pa);
        [pb_n, ~] = normalize_points(pa);
        if size(pvm,1) == 0
            % if pvm is empty, add all points
            pvm = [pa(1,:);pa(2,:);pb(1,:);pb(2,:)];
            pvm_n = [pa_n(1,:);pa_n(2,:);pb_n(1,:);pb_n(2,:)];
        else
            % else add, empty rows
            pvm = [pvm;zeros(2,size(pvm,2))];       %add image row
            pvm_n = [pvm_n;zeros(2,size(pvm_n,2))]; %add image row
            prev = pvm(end-3:end-2,:);
            prev_n = pvm_n(end-3:end-2,:);
            % iterate over point correspondences
            for p = 1:size(pa,2)
                [min_dist, p_idx] = min(sqrt(sum( (pa_n(1:2,p) - prev_n).^2 )));
                if min_dist < thresh
                    % if the point is already in the pvm, add to
                    % corresponding column
                    pvm(end-1:end,p_idx) = pb(1:2,p);
                    pvm_n(end-1:end,p_idx) = pb_n(1:2,p);
                else
                    % else, add new column and add coords to column
                    pvm = [pvm, zeros(size(pvm,1),1)];
                    pvm_n = [pvm_n, zeros(size(pvm_n,1),1)];
                    pvm(end-3:end,end) = [pa(1:2,p);pb(1:2,p)];
                    pvm_n(end-3:end,end) = [pa_n(1:2,p);pb_n(1:2,p)];
                end
            end
        end
    end
    
    %filter zero-values 
    for i = size(pvm,2):-1:1
        if sum(pvm(:,i)==0) > frames_absent*2
            pvm(:,i) = [];
        end
    end
    
    if plot
        %plot chains as scatter
        figure(1)
        imshow(get_house_frame("Data/House/House",1))
        hold on
        for j = 1:2:size(pvm,1)
            scatter(pvm(j,:),pvm(j+1,:))
        end
        hold off
        
        %plot matrix itself
        figure(2)
        imshow(pvm>0)
    end
end