#!/usr/bin/env python3
"""
Demo script for video processing with Llama APIs and AWS Polly dubbing.
"""

import os
import json
from app.services.video_processor import VideoProcessor


def demo_video_analysis():
    """Demo video analysis functionality."""
    print("=== Video Analysis Demo ===")
    
    processor = VideoProcessor()
    
    # Example video path (replace with actual video file)
    video_path = "sample_video.mp4"
    
    if not os.path.exists(video_path):
        print(f"Video file {video_path} not found. Please upload a video first.")
        return
    
    print(f"Analyzing video: {video_path}")
    
    # Analyze video content
    result = processor.process_video_analysis_only(video_path)
    
    if result["success"]:
        print("✅ Video analysis completed successfully!")
        print(f"Video insights: {result['video_insights']}")
        print(f"Generated scripts for {len(result['scripts'])} perspectives")
        
        # Show sample script
        for perspective, script in result['scripts'].items():
            print(f"\n--- {perspective.upper()} PERSPECTIVE ---")
            print(script[:200] + "..." if len(script) > 200 else script)
    else:
        print(f"❌ Analysis failed: {result['error']}")


def demo_audio_dubbing():
    """Demo audio dubbing functionality."""
    print("\n=== Audio Dubbing Demo ===")
    
    processor = VideoProcessor()
    
    # Sample script
    sample_script = """
    Welcome to this comprehensive analysis. In this video, we explore the fascinating 
    world of data visualization and its impact on modern business intelligence. 
    The charts and graphs presented here demonstrate clear trends in market performance, 
    showing significant growth in key metrics over the past quarter.
    """
    
    video_path = "sample_video.mp4"
    output_dir = "output"
    
    if not os.path.exists(video_path):
        print(f"Video file {video_path} not found. Using mock processing.")
        video_path = "mock_video.mp4"
    
    print("Generating audio dubs for different perspectives...")
    
    # Generate audio for different perspectives
    perspectives = ["educational", "entertaining", "professional"]
    
    for perspective in perspectives:
        print(f"\nProcessing {perspective} perspective...")
        result = processor.process_audio_only(sample_script, video_path, output_dir, perspective)
        
        if result["success"]:
            print(f"✅ {perspective} audio generated successfully!")
            print(f"   Voice used: {result['audio_data']['voice_used']}")
            print(f"   Duration: {result['audio_data']['total_duration']:.2f} seconds")
        else:
            print(f"❌ {perspective} audio failed: {result['error']}")


def demo_complete_pipeline():
    """Demo complete video processing pipeline."""
    print("\n=== Complete Pipeline Demo ===")
    
    processor = VideoProcessor()
    
    video_path = "sample_video.mp4"
    output_dir = "complete_output"
    
    if not os.path.exists(video_path):
        print(f"Video file {video_path} not found. Please upload a video first.")
        return
    
    print(f"Processing complete pipeline for: {video_path}")
    print("This will: 1) Analyze video, 2) Generate scripts, 3) Create audio dubs, 4) Sync with video")
    
    # Process with specific perspectives
    perspectives = ["educational", "professional"]
    result = processor.process_video_complete(video_path, output_dir, perspectives)
    
    if result["success"]:
        print("✅ Complete pipeline finished successfully!")
        print(f"Output directory: {result['output_directory']}")
        print(f"Generated {len(result['final_videos'])} final videos")
        
        for perspective, video_result in result['final_videos'].items():
            if video_result['success']:
                print(f"   ✅ {perspective}: {video_result['output_path']}")
            else:
                print(f"   ❌ {perspective}: {video_result['error']}")
    else:
        print(f"❌ Pipeline failed: {result['error']}")


def demo_batch_processing():
    """Demo batch processing of multiple videos."""
    print("\n=== Batch Processing Demo ===")
    
    processor = VideoProcessor()
    
    # Example video paths (replace with actual video files)
    video_paths = ["video1.mp4", "video2.mp4", "video3.mp4"]
    
    # Filter to only existing videos
    existing_videos = [path for path in video_paths if os.path.exists(path)]
    
    if not existing_videos:
        print("No video files found. Please upload videos first.")
        return
    
    print(f"Processing {len(existing_videos)} videos in batch...")
    
    result = processor.batch_process_videos(existing_videos, "batch_output")
    
    if result["success"]:
        print(f"✅ Batch processing completed!")
        print(f"Total videos: {result['total_videos']}")
        print(f"Successfully processed: {result['processed_videos']}")
        
        for video_name, video_result in result['results'].items():
            status = "✅" if video_result['success'] else "❌"
            print(f"   {status} {video_name}")
    else:
        print(f"❌ Batch processing failed: {result['error']}")


def main():
    """Run all demos."""
    print("🎬 Video Processing with Llama APIs and AWS Polly Demo")
    print("=" * 60)
    
    # Check if required environment variables are set
    required_vars = [
        "LLAMA4_API_KEY", "LLAMA4_API_BASE", 
        "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        print("Some demos may not work without proper API keys.")
    
    # Run demos
    try:
        demo_video_analysis()
        demo_audio_dubbing()
        demo_complete_pipeline()
        demo_batch_processing()
        
        print("\n🎉 All demos completed!")
        print("\nTo use the API endpoints:")
        print("1. Start the server: python -m uvicorn app.main:app --reload")
        print("2. Visit: http://localhost:8000/docs")
        print("3. Try the video processing endpoints")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure all dependencies are installed and API keys are configured.")


if __name__ == "__main__":
    main() 