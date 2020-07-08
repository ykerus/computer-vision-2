function [] = ICP_analytics(folder, index1, index2, runs_per_method)
    % Run analytics of all sampling techniques given the
    % source.mat and target.mat files
    [base, normal] = getPcd(folder, index1);
    [target, target_normal] = getPcd(folder, index2);
    
    sampling_technique = ["all", "uniform", "random", "informed"];
    
    for st = sampling_technique
        RMSfs = [];
        times = [];
        for run = 1:runs_per_method
            display("Evaluating " + st + ", Run: " + run);
            [bt, RMS, Rf, tf, RMSf, time] = ICP(base,target,normal,target_normal,100,st,5000,true, false);
            RMSfs(end+1) = RMSf;
            times(end+1) = time;
        end  
        display("--------------------------------");
        display("Mean RMSf: " + mean(RMSfs));
        display("STD RMSf: " + std(RMSfs));
        display("Variance RMSf: " + var(RMSfs));
        display("Mean time: " + mean(times));
        display("STD time: " + std(times));
        display("Variance time: " + var(times));
    end
    
end

