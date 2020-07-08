function F = eight_point_alg(p1, p2)
    % INPUT
    % I1 - image 1
    % I2 - image 2
    %
    % OUTPUT
    % f - the fundamental matrix
    
    % Get the matching points 
    % -> done in calling function get_F
        
    % Construct n x 9 matrix A
    A = [];
    
    % Loop over all matches
    for i = 1:size(p1,2) % match i
        row = reshape((p1(:,i) * p2(:,i)'), [1,9]);
        A = [A; row];
    end
    
    % Perform SVD on A
    [~,D,V] = svd(A);
    
    % Get smallest singular value and index
    [~, min_id] = min(diag(D));
    
    % Get components of the column of V corresponding 
    % to the smallest singular value
    F = V(:,min_id);
    
    % reshape to 3x3
    F = reshape(F, [3,3]);
    
    % Perform svd on F
    [Uf, Df, Vf] = svd(F);
    
    % Set smallest sv of diag Df to zero
    [~, min_idf] = min(diag(Df));
    Df(min_idf, min_idf) = 0;
    
    % Recompute F
    F = Uf*Df*Vf';
    
    % Test F
%     F_test = reshape(F, [9,1]);
%     disp((A*F_test));
      
end