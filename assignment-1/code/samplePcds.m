function [pcd1, pcd2] = samplePcds(pcd1, pcd2, n1, n2, sampling, Npoints)
    % sampling = {"all", "uniform", "random", "informed"}
    % Npoints is ignored if sampling = "all"
    % sampling = {"all", "uniform", "random", "informed"}
    % Npoints is ignored if sampling = "all"
    
    size1 = size(pcd1,2);
    size2 = size(pcd2,2);
    
    if sampling == "informed"
        pcd1 = sampleNormal(pcd1, n1, Npoints);
        pcd2 = sampleNormal(pcd2, n2, Npoints);
    else
        if sampling == "all"
%             % Make base and target equal size
%             if size1 > size2
%                 sample1 = randsample(size1, size2);
%                 sample2 = 1:size2;
%             elseif size2 > size1
%                 sample1 = 1:size1;
%                 sample2 = randsample(size2, size1);
%             else
            sample1 = 1:size1;
            sample2 = 1:size2;
%             end
        elseif sampling == "uniform" || sampling == "random"
            sample1 = randsample(size1, Npoints);
            sample2 = randsample(size2, Npoints);
        end
        pcd1 = pcd1(:,sample1);
        pcd2 = pcd2(:,sample2);
    end
end