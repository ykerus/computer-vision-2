function showPcd(pcd)
X = [ pcd(1,:)];
Y = [ pcd(2,:)];
Z = [ pcd(3,:)];
C = [ pcd(4,:)];
fscatter3(X, Y, Z, C, winter)
end