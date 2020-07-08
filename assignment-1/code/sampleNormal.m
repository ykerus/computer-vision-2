function pcd = sampleNormal(pcd, normal, Npoints)

    % Filter nans
    pcd(:,isnan(normal(1,:))) = [];
    normal(:,isnan(normal(1,:))) = [];
    
    % Bin edges (same for each dimension)
    E = [-1, -.5, 0, .5, 1];
    
    % Bin each dimension separately
    Y1 = discretize(normal(1,:), E);
    Y2 = discretize(normal(2,:), E);
    Y3 = discretize(normal(3,:), E);
    
    % Now discretize points in 3-D space
    clusters = Y1*100+Y2*10+Y3;
    bins = length(unique(clusters));
    Y = discretize(clusters, [sort(unique(clusters)),1e3]);
    
    % Sample uniformly from bins
    temp = [];
    notSampled = [];
    binPoints = round(Npoints/bins);
    for i = 1:bins
        bin = pcd(:,Y==i);
        binSize = size(bin,2);
        if binSize <= binPoints
            sample = 1:binSize;
        else
            shuffled = randsample(binSize, binSize);
            sample = shuffled(1:binPoints);
            notSampled = [notSampled, bin(:,shuffled(binPoints+1:end))];
        end
        temp = [temp , bin(:,sample)];
    end
    
    % Sample the leftovers uniformly over all points
    leftOver = Npoints - size(temp,2);
    sample = randsample(size(notSampled,2), leftOver);
    temp = [temp , notSampled(:,sample)];
    
    % print how many bins were used
%     bins
    
    pcd = temp;

end