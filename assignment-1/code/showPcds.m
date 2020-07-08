function showPcds(pcd1, pcd2)

X = [ pcd1(1,:)' ; pcd2(1,:)' ];
Y = [ pcd1(2,:)' ; pcd2(2,:)' ];
Z = [ pcd1(3,:)' ; pcd2(3,:)' ];
C = [ pcd1(4,:)' ; pcd2(4,:)' ];
fscatter3(X, Y, Z, C, winter)

end