function fullMerge(stepsize, sampling, folder)
    [base,nbase] = getPcd(folder, 0);
    showPcd(base)
    prev = base;
    prevn = nbase;
    for i = stepsize:stepsize:99
        [pcd,n] = getPcd(folder, i);
        [pcdTF,~,~,~,~,~] = ICP(pcd, prev, n, prevn, 30, sampling, 5000, false, false);
        prev = pcdTF;
        prevn = n;
        showPcd(pcdTF)
    end
end