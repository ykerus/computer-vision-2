function [I] = get_house_frame(folder, index)
    % INPUT
    % folder - folder containing all house images
    % index - index of house image
    %
    % OUTPUT
    % I - read image from folder.

    if index < 1 || index > 49
        error("Index does not exist.");
    end
    
    if index < 10
        fname = folder + '/frame0000000' + index + '.png';
    else
        fname = folder + '/frame000000' + index + '.png';
    end
    
    I = imread(char(fname));
    
end