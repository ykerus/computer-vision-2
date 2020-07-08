function printRMS(RMS)
    toprint = "[";
    for i = 1:length(RMS)
        toprint = toprint + RMS(i);
        if i < length(RMS)
            toprint = toprint + ",";
        end
    end
    toprint = toprint +"]";
    disp(toprint)    
end