function [pcd, normal] = processPcd(pcd, normal)
 
threshold = 1.5;

pcd = pcd(:,1:4)';
normal = normal(:,1:3)';

background = pcd(3,:) > threshold;

pcd(:,background) = [];
normal(:,background) = [];

end