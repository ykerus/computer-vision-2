function d = sampson_dist(p1, p2, F)
    % calculate sampson distance as specified in the assignment

    d = zeros(1,size(p1,2),1);
    for j = 1:size(p1,2)
        Fp1j = F * p1(:,j);
        Fp2j = F' * p2(:,j);
        denominator = Fp1j(1)^2 + Fp1j(2)^2 + Fp2j(1)^2 + Fp2j(2)^2;
        d(j) = (p2(:,j)' * Fp1j)^2 / denominator;
    end
    
end