#!/usr/bin/env swift
import Cocoa
import Vision

guard CommandLine.arguments.count > 1 else {
    fputs("Usage: detect-image-text.swift <image.png>\n", stderr)
    exit(2)
}

let path = CommandLine.arguments[1]
let url = URL(fileURLWithPath: path)
guard let image = NSImage(contentsOf: url) else { exit(1) }
var rect = NSRect(origin: .zero, size: image.size)
guard let cg = image.cgImage(forProposedRect: &rect, context: nil, hints: nil) else { exit(1) }

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
do {
    try handler.perform([request])
} catch {
    exit(1)
}

var lines: [String] = []
for obs in request.results ?? [] {
    if let top = obs.topCandidates(1).first, top.confidence > 0.25 {
        let t = top.string.trimmingCharacters(in: .whitespacesAndNewlines)
        if !t.isEmpty { lines.append(t) }
    }
}
print(lines.joined(separator: "\n"))
