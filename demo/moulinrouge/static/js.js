function calculateAreaOfPolygon(vertices) {
    let area = 0;
    for (let i = 0; i < vertices.length; i++) {
        const x1 = vertices[i][0];
        const y1 = vertices[i][1];
        const x2 = vertices[(i + 1) % vertices.length][0];
        const y2 = vertices[(i + 1) % vertices.length][1];
        
        // Calculate the area of a triangle formed by the point (x1, y1), 
        // (x2, y2), and (x3, y3)
        let base = Math.abs((y2 - y1) * x1 - (x2 - x1) * y1);
        let height = Math.abs((y3 - y1) / 2 - (x3 - x1) / 2);
        
        if ((base > 0 && height > 0)) {
            area += base * height;
        }
    }
    return area;
}