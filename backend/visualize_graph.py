#!/usr/bin/env python3
"""
LangGraph Visualization Script for ReplySight Workflow.

This script generates and displays the ReplySight workflow graph
using LangGraph's built-in visualization capabilities with enhanced
production deployment features.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from backend.graph import create_replysight_graph


def generate_workflow_diagram(output_path: str = "replysight_workflow.png", 
                            format_type: str = "png") -> Dict[str, Any]:
    """
    Generate workflow diagram for production deployment.
    
    Args:
        output_path: Path where to save the diagram
        format_type: Output format (png, mermaid, json)
        
    Returns:
        Result metadata
    """
    print("🚀 Generating ReplySight Workflow Visualization...")
    print("=" * 60)
    
    try:
        graph = create_replysight_graph()
        print("✅ Graph created successfully!")
        
        if format_type == "png":
            result = graph.save_graph_diagram(output_path)
            return {
                "status": "success",
                "format": "png",
                "output_path": output_path,
                "message": result
            }
        
        elif format_type == "mermaid":
            mermaid_code = graph.get_graph_visualization()
            with open(output_path, "w") as f:
                f.write(mermaid_code)
            return {
                "status": "success",
                "format": "mermaid",
                "output_path": output_path,
                "message": f"Mermaid diagram saved to {output_path}"
            }
        
        elif format_type == "json":
            metadata = graph.get_graph_metadata()
            with open(output_path, "w") as f:
                json.dump(metadata, f, indent=2)
            return {
                "status": "success",
                "format": "json",
                "output_path": output_path,
                "message": f"Graph metadata saved to {output_path}"
            }
        
        else:
            return {
                "status": "error",
                "error": f"Unknown format: {format_type}",
                "message": f"Supported formats: png, mermaid, json"
            }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to generate {format_type} diagram"
        }


def docker_visualization_check() -> Dict[str, Any]:
    """
    Perform visualization health check for Docker containers.
    
    Returns:
        Health check results
    """
    print("🐳 Docker Environment Visualization Check...")
    print("=" * 50)
    
    try:
        graph = create_replysight_graph()
        
        # Test graph compilation
        metadata = graph.get_graph_metadata()
        
        # Test visualization generation
        mermaid_test = graph.get_graph_visualization()
        
        # Test PNG generation (may fail in headless environments)
        png_test = "skipped"
        try:
            graph.save_graph_diagram("/tmp/test_diagram.png")
            png_test = "success"
            os.remove("/tmp/test_diagram.png")
        except Exception:
            png_test = "failed - likely headless environment"
        
        results = {
            "status": "healthy",
            "graph_compilation": "success",
            "mermaid_generation": "success" if mermaid_test else "failed",
            "png_generation": png_test,
            "node_count": metadata["node_count"],
            "edge_count": metadata["edge_count"],
            "environment": "docker" if os.path.exists("/.dockerenv") else "native"
        }
        
        print("✅ Docker visualization check passed!")
        for key, value in results.items():
            print(f"  • {key}: {value}")
        
        return results
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "message": "Docker visualization check failed"
        }


def ci_cd_pipeline_integration(output_dir: str = "./artifacts") -> Dict[str, Any]:
    """
    Generate all visualization artifacts for CI/CD pipeline.
    
    Args:
        output_dir: Directory to save all artifacts
        
    Returns:
        Generation results
    """
    print("🔄 CI/CD Pipeline Visualization Generation...")
    print("=" * 50)
    
    os.makedirs(output_dir, exist_ok=True)
    artifacts = {}
    
    try:
        graph = create_replysight_graph()
        
        # Generate Mermaid diagram for documentation
        mermaid_result = generate_workflow_diagram(
            f"{output_dir}/workflow.mmd", "mermaid"
        )
        artifacts["mermaid"] = mermaid_result
        
        # Generate JSON metadata for API documentation
        json_result = generate_workflow_diagram(
            f"{output_dir}/workflow-metadata.json", "json"
        )
        artifacts["metadata"] = json_result
        
        # Try to generate PNG for visual documentation
        png_result = generate_workflow_diagram(
            f"{output_dir}/workflow-diagram.png", "png"
        )
        artifacts["png"] = png_result
        
        # Generate deployment summary
        summary = {
            "timestamp": time.time(),
            "workflow_name": "ReplySight Customer Service Response Generator",
            "artifacts_generated": list(artifacts.keys()),
            "visualization_urls": {
                "mermaid_live": "https://mermaid.live",
                "documentation": f"{output_dir}/workflow.mmd"
            },
            "deployment_ready": all(
                artifact["status"] == "success" 
                for artifact in artifacts.values()
            )
        }
        
        with open(f"{output_dir}/deployment-summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print("✅ CI/CD artifacts generated successfully!")
        print(f"📁 Artifacts saved to: {output_dir}")
        
        return {
            "status": "success",
            "artifacts": artifacts,
            "summary": summary,
            "output_directory": output_dir
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "CI/CD pipeline generation failed"
        }


def monitoring_dashboard_export(output_file: str = "monitoring-config.json") -> Dict[str, Any]:
    """
    Export configuration for monitoring dashboards (Grafana, DataDog, etc.).
    
    Args:
        output_file: Path to save monitoring configuration
        
    Returns:
        Export results
    """
    print("📊 Monitoring Dashboard Configuration Export...")
    print("=" * 50)
    
    try:
        graph = create_replysight_graph()
        metadata = graph.get_graph_metadata()
        
        # Generate monitoring configuration
        monitoring_config = {
            "workflow_metrics": {
                "name": metadata["workflow_name"],
                "nodes": metadata["nodes"],
                "edges": metadata["edges"],
                "critical_path": ["START", "fetch_parallel", "compose_response", "END"],
                
                # Suggested monitoring points
                "monitoring_points": {
                    "fetch_parallel": {
                        "metrics": ["latency", "success_rate", "parallel_efficiency"],
                        "alerts": ["latency > 2000ms", "success_rate < 0.95"]
                    },
                    "compose_response": {
                        "metrics": ["llm_latency", "token_usage", "quality_score"],
                        "alerts": ["latency > 3000ms", "token_usage > 1000"]
                    }
                },
                
                # Grafana dashboard suggestions
                "grafana_panels": [
                    {
                        "title": "Workflow Latency",
                        "type": "timeseries",
                        "targets": ["workflow_total_latency", "node_latencies"]
                    },
                    {
                        "title": "Success Rate",
                        "type": "stat",
                        "targets": ["workflow_success_rate"]
                    },
                    {
                        "title": "Cost per Request",
                        "type": "timeseries", 
                        "targets": ["api_costs", "llm_costs"]
                    }
                ]
            },
            
            "langsmith_integration": {
                "enabled": bool(os.getenv("LANGCHAIN_TRACING_V2")),
                "project": "replysight-production",
                "trace_sampling": 1.0
            },
            
            "visualization": {
                "mermaid_diagram": metadata["mermaid_diagram"],
                "update_frequency": "on_deployment",
                "embedding_instructions": "Use /workflow/graph API endpoint"
            }
        }
        
        with open(output_file, "w") as f:
            json.dump(monitoring_config, f, indent=2)
        
        print(f"✅ Monitoring configuration exported to {output_file}")
        
        return {
            "status": "success",
            "config_file": output_file,
            "monitoring_points": len(monitoring_config["workflow_metrics"]["monitoring_points"]),
            "message": "Monitoring dashboard configuration ready"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Monitoring export failed"
        }


def main():
    """
    Enhanced main function with command-line argument support.
    """
    parser = argparse.ArgumentParser(
        description="ReplySight Workflow Visualization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python visualize_graph.py                          # Interactive mode
  python visualize_graph.py --ci-cd                  # CI/CD pipeline mode
  python visualize_graph.py --docker-check           # Docker health check
  python visualize_graph.py --monitoring-export      # Export monitoring config
  python visualize_graph.py --output diagram.png --format png  # Custom output
        """
    )
    
    parser.add_argument("--ci-cd", action="store_true",
                      help="Generate artifacts for CI/CD pipeline")
    parser.add_argument("--docker-check", action="store_true", 
                      help="Perform Docker environment health check")
    parser.add_argument("--monitoring-export", action="store_true",
                      help="Export monitoring dashboard configuration")
    parser.add_argument("--output", type=str, default="replysight_workflow.png",
                      help="Output file path")
    parser.add_argument("--format", choices=["png", "mermaid", "json"], 
                      default="png", help="Output format")
    parser.add_argument("--quiet", action="store_true",
                      help="Suppress verbose output")
    
    args = parser.parse_args()
    
    if args.ci_cd:
        result = ci_cd_pipeline_integration()
        if not args.quiet:
            print(json.dumps(result, indent=2))
        return 0 if result["status"] == "success" else 1
    
    elif args.docker_check:
        result = docker_visualization_check()
        if not args.quiet:
            print(json.dumps(result, indent=2))
        return 0 if result["status"] == "healthy" else 1
    
    elif args.monitoring_export:
        result = monitoring_dashboard_export()
        if not args.quiet:
            print(json.dumps(result, indent=2))
        return 0 if result["status"] == "success" else 1
    
    else:
        # Interactive mode (original functionality)
        if not args.quiet:
            print("🚀 Generating ReplySight Workflow Visualization...")
            print("=" * 60)
        
        # Create the graph
        try:
            graph = create_replysight_graph()
            if not args.quiet:
                print("✅ Graph created successfully!")
        except Exception as e:
            print(f"❌ Error creating graph: {e}")
            return 1
        
        # Generate requested format
        result = generate_workflow_diagram(args.output, args.format)
        
        if not args.quiet:
            # Print detailed structure
            print("\n📊 Graph Structure Analysis:")
            graph.print_graph_structure()
            
            # Get metadata
            metadata = graph.get_graph_metadata()
            print(f"\n📋 Workflow Metadata:")
            print(f"  • Name: {metadata['workflow_name']}")
            print(f"  • Nodes: {metadata['node_count']}")
            print(f"  • Edges: {metadata['edge_count']}")
            
            # Print execution flow
            print(f"\n🔄 Execution Flow:")
            for step in metadata['execution_flow']:
                print(f"  {step}")
            
            print(f"\n💾 Output:")
            print(f"  {result['message']}")
            
            if args.format == "mermaid":
                print(f"\n🌐 Web-Ready Mermaid Diagram:")
                print("=" * 40)
                mermaid_code = graph.get_graph_visualization()
                print(mermaid_code)
                print("=" * 40)
                print(f"🔗 Copy the above to https://mermaid.live for interactive viewing")
            
            print(f"\n✨ Visualization Complete!")
        
        return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main()) 