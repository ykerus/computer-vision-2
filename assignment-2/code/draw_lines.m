function draw_lines(I1, I2, p1, p2, F, sample)
    % draws epilines over images I1 and I2 using F
    sampleN = 10; 
    if sample
        % sample 10 points, and thus epilines
        sample = randsample(size(p1,2), sampleN);
        p1 = p1(:,sample);
        p2 = p2(:,sample);
    end
    
    %define x-range
    x = linspace(0, size(I1,2));
    subplot(1,2,1);
    imshow(I1)
    hold on
    for i = 1:size(p1,2)
        %plot each point in the left image with the lines obtained with F
        %and the points from the right image
        p_right = p2(:,i);
        pF_left = F' * p_right;
        y_left = -(pF_left(1)*x + pF_left(3))/pF_left(2);
        l = plot(x, y_left);
        scatter(p1(1,i),p1(2,i),25, l.Color)
       
    end
    hold off
    drawnow
    subplot(1,2,2);
    imshow(I2)
    hold on
    for i = 1:size(p2,2)
        %plot each point in the right image with the lines obtained with F
        %and the points from the left image
        p_left = p1(:,i);
        pF_right = F * p_left;
        y_right = -(pF_right(1)*x + pF_right(3))/pF_right(2);
        l = plot(x, y_right);
        scatter(p2(1,i),p2(2,i),25, l.Color)
        
    end
    hold off
    drawnow
    
end

