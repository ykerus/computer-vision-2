function SFM_demo(gather_method, file)
    % Gather method - empty (only add point if point was not
    % added yet) override (override each new set of points from dense
    % block)
    % file - false (use chaining method) true (use file)
    % Make sure that the PointViewMatrix.txt file is in the same folder!
    if file == true
        pvm = load("PointViewMatrix.txt");
        threshold = 40;
    else
        pvm = chaining(30, false);
        threshold = 9;
    end
    
    if gather_method == "empty"
        SFM(pvm, "empty",threshold, true);
    else
        SFM(pvm, "override",threshold, true);
    end
end