function norm_dense = normalize_SFM(pvm)
    
    % From slide 70
    center = mean(pvm, 2);
    norm_dense = pvm - center;
end