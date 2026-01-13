export function MeshBackground() {
  return (
    <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none">
      <div className="absolute inset-0 bg-background" />
      <div 
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage: `
            radial-gradient(circle at 15% 50%, rgba(14, 165, 233, 0.4), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.4), transparent 25%),
            radial-gradient(circle at 50% 80%, rgba(251, 146, 60, 0.2), transparent 40%)
          `,
          filter: "blur(40px)",
        }}
      />
      
      {/* Animated orbs Layer - we can make this move with GSAP if needed. 
          For now, static gradient stack provides a good base. 
      */}
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.03]" /> 
    </div>
  );
}
