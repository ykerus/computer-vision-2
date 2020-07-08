function [pcd, normal] = getPcd(folder, index)
% folder - folder where data is located
% index - index of image

if index > 9
    fname = "00000000" + index;
else
    fname = "000000000" + index;
end

pcd = readPcd(folder + "/" + fname + ".pcd");
normal = readPcd(folder + "/" + fname + "_normal.pcd");
[pcd, normal] = processPcd(pcd, normal);

end