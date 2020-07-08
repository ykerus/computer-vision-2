function [pn, T] = normalize_points(p)
    %returns normalized points pn and normalization matrix T

    m = mean(p, 2); %mx = m(1), my = m(2)
    d = mean(sqrt((p(1,:) - m(1)).^2 + (p(2,:) - m(2)).^2));
    
    T = [sqrt(2)/d     0       -m(1)*sqrt(2)/d;
             0     sqrt(2)/d   -m(2)*sqrt(2)/d;
             0          0            1       ];
         
    pn = T*p;
    
end